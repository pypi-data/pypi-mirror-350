import json
import logging
from collections.abc import Mapping
from pathlib import Path
from typing import cast

import numpy as np
import pandas as pd
from dask.distributed import Client, Future
from numpy.typing import NDArray
from rich.progress import Progress

from apb.application.tmalign.core import ALLOWED_TMALIGN_EXTENSIONS, TMAlignOutput, run_tmalign
from apb.structure.utils import extension_matches
from apb.types import Pathish
from apb.utils import Timer, converter

# Dask & dask.distributed outputs more logging than we're interested in
logging.getLogger("dask").setLevel(logging.ERROR)
logging.getLogger("distributed").setLevel(logging.ERROR)

ManyToManyOutput = dict[str, dict[str, TMAlignOutput]]


def _build_from_inverse(inverse: TMAlignOutput) -> TMAlignOutput:
    return TMAlignOutput(
        qseq_aligned=inverse.tseq_aligned,
        tseq_aligned=inverse.qseq_aligned,
        qtmscore=inverse.ttmscore,
        ttmscore=inverse.qtmscore,
        rmsd=inverse.rmsd,
    )


def _validate_paths(paths: list[Pathish]) -> None:
    if not all(extension_matches(path, ALLOWED_TMALIGN_EXTENSIONS) for path in paths):
        raise ValueError(f"TMalign only accepts the extensions: {ALLOWED_TMALIGN_EXTENSIONS}")


def _submit_batch(
    batch: list[tuple[str, str]],
    client: Client,
    results: ManyToManyOutput,
    query_structures: Mapping[str, Pathish],
    target_structures: Mapping[str, Pathish],
) -> dict[str, dict[str, Future]]:
    """Submit a batch of TMalign jobs.

    The TMalign jobs are submitted in batches to avoid overloading the scheduler.
    Anecdotally, dask slows down substantially when the scheduler holds >500k jobs
    concurrently, even if the jobs are largely independent of one another. Understanding
    the circumstances of the slow-down would be useful, but batching is good practice in
    general and alleviates the problem.

    Args:
        batch:
            A list of two-ples, where the first and second elements are the
            structure identifiers of the query and target, respectively.
    """
    futures: dict[str, dict[str, Future]] = {}
    for query, target in batch:
        if query not in futures:
            futures[query] = {}

        # In what follows, we check if the inverse alignment has been calculated or
        # submitted. Since the alignment of query to target can be derived from the
        # alignment of target to query (see _build_from_inverse to see how), we can
        # build the alignment from its inverse, assuming the inverse has been or
        # will be calculated.

        if target in results and query in results[target]:
            # The inverse is in `results`, meaning it's already been calculated.
            future = client.submit(_build_from_inverse, results[target][query])
        elif target in futures and query in futures[target]:
            # The inverse is in `futures`, meaning it's been submitted. The job may
            # or may not be complete, but either way, we pass the `Future` object to
            # `client.submit` and the alignment will be built from its inverse when
            # ready.
            future = client.submit(_build_from_inverse, futures[target][query])
        else:
            future = client.submit(run_tmalign, query_structures[query], target_structures[target])

        futures[query][target] = future

    return futures


def align_many_to_many(
    query_structures: Mapping[str, Pathish],
    target_structures: Mapping[str, Pathish],
    client: Client,
    batch_size: int = 2000,
) -> ManyToManyOutput:
    """Perform many-to-many structure alignments using TMalign.

    This function computes all pairwise alignments between structures in
    `query_structures` and `target_structures` using TMalign.

    The computation is parallelized with Dask. If a Dask client is not provided, a new
    client will be created for the duration of the computation.

    The computation is also sped up by leveraging that TMalign has an inverse
    relationship with its inputs, whereby the alignment of query to target can be
    derived from the inverse alignment (target to query). By building alignments
    from their inverses, where possible, the amount of explicit calculation required is
    reduced by as much as half depending on the amount of query/target overlap.

    Args:
        query_structures:
            A mapping from structure identifiers to file paths for the query structures.
        target_structures:
            A mapping from structure identifiers to file paths for the target
            structures.
        client:
            A Dask client to use for computation. If None, a new client will be created.
            Defaults to None.
        batch_size:
            The number of alignments to submit per batch.

    Returns:
        dict[str, dict[str, TMAlignOutput]]:
            A nested dictionary containing the alignment results. The outer dictionary
            is keyed by query structure identifiers, and the inner dictionary is keyed
            by target structure identifiers. Each value is a `TMAlignOutput` object
            containing the alignment results.

    Raises:
        ValueError:
            If any of the file paths do not have an extension expected by TMalign.
    """

    # Vet all the paths prior to starting (many-to-many could be an expensive op).
    _validate_paths(list(query_structures.values()) + list(target_structures.values()))

    logging.info(f"View status: {client.dashboard_link}")
    logging.info(f"Progress updates every {batch_size} comparisons")

    results: ManyToManyOutput = {}
    num_comparisons = len(query_structures) * len(target_structures)
    total_batches = (num_comparisons + batch_size - 1) // batch_size
    query_target_pairs = [
        (query, target) for query in query_structures for target in target_structures
    ]

    with Progress(transient=True) as progress, Timer(quiet=True) as timer:
        task = progress.add_task(description="", total=num_comparisons)

        for batch_num in range(total_batches):
            count = batch_num * batch_size

            progress.update(task, description=f"Performing alignments [{count}/{num_comparisons}]")

            batch = query_target_pairs[count : count + batch_size]
            futures = _submit_batch(batch, client, results, query_structures, target_structures)

            # `client.gather` returns the same type passed to it, except with all `Future`
            # objects replaced with their results. We inform our type checker of this by
            # casting the type explictly.
            batch_results = cast(ManyToManyOutput, client.gather(futures))

            # Populate `results` with the results of the batch.
            for query, target_results in batch_results.items():
                results.setdefault(query, {}).update(target_results)

            progress.advance(task, len(batch))

    logging.info(f"{num_comparisons} alignments calculated in {timer.time}")

    return results


def load_alignments_json(path: Pathish) -> ManyToManyOutput:
    with open(path) as fp:
        return converter.structure(json.load(fp), ManyToManyOutput)


def save_alignments_json(path: Pathish, alignments: ManyToManyOutput) -> Path:
    with open(path, "w") as fp:
        json.dump(converter.unstructure(alignments), fp, indent=2)

    return Path(path)


def align_to_reference(
    reference_structure: Pathish,
    target_structures: Mapping[str, Pathish],
    client: Client,
) -> pd.DataFrame:
    """Performs alignment of a collection of structures to a reference structure using TMalign.

    Executes a pairwise alignment to the reference structure for each target structure
    and returns the alignment trace.

    Args:
        reference_structure: Path to the reference structure file.
        target_structures:
            A mapping from structure identifiers to file paths for the target structures.

    Returns:
        pd.DataFrame:
            A dataframe of the alignment trace. Each column is a target hit to the
            reference. The indices are the reference residue indices. For further
            details, see `apb.utils.StructuralReferenceAligner`.
    """
    alignments = align_many_to_many({"ref": reference_structure}, target_structures, client)["ref"]

    traces: dict[str, NDArray[np.int64]] = {}
    for target, alignment in alignments.items():
        biotite_alignment = alignment.to_biotite()
        target_trace = biotite_alignment.trace[:, 1]
        reference_trace = biotite_alignment.trace[:, 0]

        # Remove all align indices in the target where the reference is gapped.
        target_trace = target_trace[reference_trace != -1]

        traces[target] = target_trace

    return pd.DataFrame(traces)
