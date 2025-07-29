from __future__ import annotations
from collections.abc import Mapping
from functools import partial

import attrs
import numpy as np
import pandas as pd
from biotite.sequence.align.cigar import read_alignment_from_cigar
from biotite.sequence.seqtypes import ProteinSequence
from numpy.typing import NDArray

from apb.application.foldseek.base import (
    DEFAULT_CONVERTALIS_CONFIG,
    DEFAULT_SEARCH_CONFIG,
    convertalis,
    createdb,
    search,
)
from apb.application.foldseek.datatypes import FoldSeekConvertalisConfig, FoldSeekSearchConfig
from apb.application.foldseek.utils import create_tsv_for_createdb
from apb.types import Pathish, StructuralReferenceAligner
from apb.utils import maybe_temp_directory

DEFAULT_REFERENCE_ALIGNMENT_SEARCH_CONFIG = attrs.evolve(DEFAULT_SEARCH_CONFIG, backtrace=True)
DEFAULT_REFERENCE_ALIGNMENT_CONVERTALIS_CONFIG = attrs.evolve(DEFAULT_CONVERTALIS_CONFIG)
CIGAR_OUTPUT_FORMAT = "query,target,qstart,tstart,qend,tend,qseq,tseq,cigar"


def _ensure_valid_search_config(config: FoldSeekSearchConfig) -> None:
    if not config.backtrace:
        raise ValueError("Cannot pass search config with backtrace=False.")


def _generate_cigar_strings(
    query_path: Pathish,
    target_path: Pathish,
    search_config: FoldSeekSearchConfig,
    convertalis_config: FoldSeekConvertalisConfig,
    working_dir: Pathish | None = None,
) -> pd.DataFrame:
    """Generates CIGAR strings for the alignments.

    This runs `foldseek search` followed by `foldseek convertalis` with the output
    format defined by `CIGAR_OUTPUT_FORMAT.

    Returns:
        pd.DataFrame: A dataframe of the resultant hits table.
    """
    convertalis_config = attrs.evolve(convertalis_config, format_output=CIGAR_OUTPUT_FORMAT)

    with maybe_temp_directory(working_dir) as working_dir:
        alignment_path = working_dir / "aln"
        output_path = working_dir / "output.tsv"

        search(query_path, target_path, alignment_path, search_config)

        hit_table = convertalis(
            query_path=query_path,
            target_path=target_path,
            alignment_path_prefix=alignment_path,
            tsv_path=output_path,
            config=convertalis_config,
            working_dir=working_dir,
        )

    return hit_table


def _process_cigar_strings(cigars: pd.DataFrame) -> pd.DataFrame:
    """Creates an alignment trace from a cigar string hit table

    This accumulates pairwise alignment traces for each hit to the reference. The final
    result is compiled into a dataframe, where the index length equals the reference
    sequence length, and each column holds the trace values for the targets that aligned
    to the reference.

    Returns:
        pd.DataFrame: A dataframe of the alignment trace.
    """
    if cigars.empty:
        raise ValueError("There are 0 hits to align.")

    # The reference sequence is in the qseq column. Grab its length from the first entry.
    ref_length = len(cigars.iloc[0].qseq)

    traces: dict[str, NDArray[np.int64]] = {}
    for _, hit in cigars.iterrows():
        # Foldseek outputs cigar strings that consume the target sequence beginning
        # from the alignment start. That means we have to splice the reference and
        # target sequences to their respective aligned segments.
        target_aligned_sequence = ProteinSequence(hit.tseq)[hit.tstart - 1 : hit.tend]
        reference_aligned_sequence = ProteinSequence(hit.qseq)[hit.qstart - 1 : hit.qend]

        # Create the alignment from the cigar string and the sequences. Confusingly,
        # we pass the target sequence to the argument `reference_sequence` and the
        # reference sequence to the argument `segment_sequence`. This is on purpose
        # and the result of biotite's opinionated nomenclature.
        alignment = read_alignment_from_cigar(
            cigar=hit.cigar,
            position=0,
            reference_sequence=target_aligned_sequence,
            segment_sequence=reference_aligned_sequence,
        )

        target_trace = alignment.trace[:, 0]
        reference_trace = alignment.trace[:, 1]

        # Since the alignment can start anywhere along the two sequences, we need to
        # offset all non-gapped (-1) trace values by the alignment start index. Note
        # that it would have sufficed to do this only for the target sequence by
        # supplying `hit.tstart - 1` to the `position` argument above (in
        # `read_alignment_from_cigar`), but for posterity we do both the target and
        # reference sequence together here:
        target_trace[target_trace > -1] += hit.tstart - 1
        reference_trace[reference_trace > -1] += hit.qstart - 1

        # Now remove all align indices in the target where the reference is gapped.
        target_trace = target_trace[reference_trace != -1]

        # The trace is currently only as long as the alignment, which varies from
        # hit to hit. To be able to compare all the traces with one another, we pad
        # each trace with the appropriate number of N-terminus and C-terminus gap
        # values (-1) such that each trace length equals the length of the
        # reference.
        n_terminal_gaps = -np.ones(hit.qstart - 1, dtype=np.int64)
        c_terminal_gaps = -np.ones(ref_length - hit.qend, dtype=np.int64)
        target_trace = np.concatenate((n_terminal_gaps, target_trace, c_terminal_gaps))

        if len(target_trace) != ref_length:
            raise RuntimeError(
                f"After concatenating N- and C-terminal gaps, the target ({hit.target}) trace "
                f"length ({len(target_trace)}) must equal the reference ({hit.query}) length "
                f"({ref_length}). The number of N- and C- terminal gap characters to pad was "
                f"calculated to be {len(n_terminal_gaps)} and {len(c_terminal_gaps)}, "
                f"respectively. Please report this issue."
            )

        traces[hit.target] = target_trace

    return pd.DataFrame(traces)


def align_to_reference(
    reference_structure: Pathish,
    target_structures: Mapping[str, Pathish],
    search_config: FoldSeekSearchConfig = DEFAULT_REFERENCE_ALIGNMENT_SEARCH_CONFIG,
    convertalis_config: FoldSeekConvertalisConfig = DEFAULT_REFERENCE_ALIGNMENT_CONVERTALIS_CONFIG,
):
    """Performs alignment of a collection of structures to a reference structure using Foldseek.

    Executes a pairwise alignment to the reference structure for each target structure
    and returns the alignment trace.

    Args:
        reference_structure: Path to the reference structure file.
        target_structures: Dictionary with keys as names and values as structure paths.
        search_config:
            Configuration for the Foldseek search. If providing this value, `backtrace`
            must be set to true, which is required for the alignment.
        convertalis_config:
            Configuration for foldseek's `convertalis` subcommand. The format_output
            attribute is ignored and overwritten with `CIGAR_OUTPUT_FORMAT`.

    Returns:
        pd.DataFrame:
            A dataframe of the alignment trace. Each column is a target hit to the
            reference. The indices are the reference residue indices. For further
            details, see `apb.utils.StructuralReferenceAligner`.

    Raises:
        ValueError: If no hits are found in the alignment process.
    """
    _ensure_valid_search_config(search_config)

    with maybe_temp_directory() as working_dir:
        query_path = working_dir / "query"
        target_path = working_dir / "target"
        target_input = working_dir / "createdb_input.tsv"

        create_tsv_for_createdb(target_input, target_structures.values())
        createdb(reference_structure, query_path)
        createdb(target_input, target_path)

        cigars = _generate_cigar_strings(
            query_path,
            target_path,
            search_config,
            convertalis_config,
            working_dir,
        )

        return _process_cigar_strings(cigars)


def create_reference_aligner(
    search_config: FoldSeekSearchConfig = DEFAULT_REFERENCE_ALIGNMENT_SEARCH_CONFIG,
    convertalis_config: FoldSeekConvertalisConfig = DEFAULT_REFERENCE_ALIGNMENT_CONVERTALIS_CONFIG,
) -> StructuralReferenceAligner:
    """Creates a structural reference aligner.

    This function configures and returns a partially applied version of
    `align_to_reference` with predefined search and convertalis configurations.

    Args:
        search_config: Configuration for the Foldseek's `search` subcommand..
        convertalis_config: Configuration for Foldseek's `convertalis` subcommand.

    Returns:
        StructuralReferenceAligner:
            A function that performs structure alignment using the specified
            configurations. See `apb.utils.StructuralReferenceAligner` for details about
            the function's inputs and outputs.
    """
    return partial(
        align_to_reference,
        search_config=search_config,
        convertalis_config=convertalis_config,
    )
