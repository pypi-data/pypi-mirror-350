from __future__ import annotations
import logging
from collections.abc import Mapping
from functools import partial

import click
import pandas as pd
import xarray as xr
from dask.distributed import Client, LocalCluster
from sqlalchemy.orm import Session

import apb.application.foldseek as foldseek
import apb.application.tmalign as tmalign
import apb.database.collection as collection
from apb.structure.convert import save_structure
from apb.structure.utils import structure_name_and_extension
from apb.types import Pathish, StructuralReferenceAligner, not_none
from apb.utils import maybe_temp_directory


def create_feature_alignment(
    aligner: StructuralReferenceAligner,
    collection_db: Pathish,
    reference_structure: Pathish,
    target_structures: Mapping[str, Pathish],
) -> xr.Dataset:
    """Creates an alignment of features from a protein collection to a reference protein.

    Implementation details: This function aligns each target protein to the reference
    protein using `aligner`. From the alignment traces, the residue features of each
    protein are mapped to the reference protein indices. This is done by creating a
    dataframe of the residue features, where the index corresponds to the indices of the
    reference protein instead of the indices of the original protein. All these pairwise
    feature alignment frames are then concatenated into a multi-index dataframe and
    finally converted into an xarray dataset.

    Args:
        aligner: The aligner object used for alignment.
        collection_db: Path to the collection database.
        reference_structure: Path to the reference structure file.
        target_structures: Dictionary with keys as names and values as structure paths.

    Returns:
        xr.Dataset: The resulting xarray dataset containing the aligned features.
    """
    traces = aligner(reference_structure, target_structures)

    aligned_frames: dict[str, pd.DataFrame] = {}

    with Session(collection.get_engine(collection_db)) as session:
        for profile in collection.iter_all_profiles(session):
            if profile.name not in traces.columns:
                # The protein didn't have a hit to the reference
                continue

            # Index is the protein trace, values are the reference trace
            ref_index = pd.Series(traces.index, index=traces[profile.name].values)

            # Drop any deletions relative to the reference
            ref_index = ref_index.loc[ref_index.index != -1]

            # Add ref_index to a copy of profile.residue_features. Now there is a
            # relationship between each residue feature and the reference index
            aligned_frame = profile.residue_features.copy()
            aligned_frame["ref_index"] = ref_index
            aligned_frame["ref_index"] = aligned_frame["ref_index"].astype("UInt32")

            # Removes insertions relative to the reference
            aligned_frame = aligned_frame.dropna(subset=["ref_index"])

            # Currently the index is the protein index. Swap the protein index with the
            # reference index
            aligned_frame = aligned_frame.reset_index().set_index("ref_index")

            aligned_frames[profile.name] = aligned_frame

    # Concatenate all the aligned frames into a multi-index, where each index specifies
    # the reference index (`ref_index`) for a given protein (`name`) residue. Note that
    # since not every alignment contains every reference index, these dataframes are all
    # of different shape, but share the same index superset: the reference indices.
    aligned_multiindex_frame = pd.concat(aligned_frames, names=["name", "ref_index"])

    # Convert to an xarray dataset. Each index level becomes a dimension, so the dataset
    # has dimensions `name` and `ref_index`. Each residue feature becomes an xarray
    # variable. The variables are defined for each reference index in every protein,
    # meaning any missing data is filled with null values. For the `amino_acid`
    # variable, we set these null values to the gap character, `-`.
    dataset = aligned_multiindex_frame.to_xarray()
    dataset["amino_acid"] = dataset["amino_acid"].fillna("-")

    return dataset


def get_preconfigured_aligners(client: Client) -> dict[str, StructuralReferenceAligner]:
    """Return the structural aligners used for aligning to reference."""
    return {
        "tmalign": partial(tmalign.align_to_reference, client=client),
        "foldseek_tmalign": foldseek.create_reference_aligner(
            search_config=foldseek.FoldSeekSearchConfig(
                backtrace=True,
                # Align the structures using Foldseek's version of the TMalign
                # algorithm (alignment_type=1). This is in contrast to doing a
                # sequence alignment of the structures' 3Di sequences. This is the
                # slowest and most accurate align option in Foldseek.
                alignment_type=1,
                # Do not perform pre-filtering (prefilter_mode=2). Pre-filtering
                # avoids comparisons of some proteins based on kmer frequencies of
                # the 3Di sequences.
                prefilter_mode=2,
                # Do not take shortcuts with TMalign-based alignment.
                tmalign_fast=0,
            ),
        ),
        "foldseek_tmalign_fast": foldseek.create_reference_aligner(
            search_config=foldseek.FoldSeekSearchConfig(
                backtrace=True,
                # Align the structures using Foldseek's version of the TMalign
                # algorithm (alignment_type=1). This is in contrast to doing a
                # sequence alignment of the structures' 3Di sequences. This is the
                # slowest and most accurate align option in Foldseek.
                alignment_type=1,
                # Do not perform pre-filtering (prefilter_mode=2). Pre-filtering
                # avoids comparisons of some proteins based on kmer frequencies of
                # the 3Di sequences.
                prefilter_mode=2,
                # Take shortcuts with the TMalign-based alignment.
                tmalign_fast=1,
            ),
        ),
        "foldseek_3di": foldseek.create_reference_aligner(
            search_config=foldseek.FoldSeekSearchConfig(
                backtrace=True,
                # Align the structures using Foldseek's 3Di+AA alignment option.
                # This is an alignment based on both the 3Di sequences and the AA
                # sequences. This is the default Foldseek option.
                alignment_type=2,
                # Do not perform pre-filtering (prefilter_mode=2). Pre-filtering
                # avoids comparisons of some proteins based on kmer frequencies of
                # the 3Di sequences.
                prefilter_mode=2,
            ),
        ),
    }


def run(
    collection_db: Pathish,
    reference_name: str,
    aligners: dict[str, StructuralReferenceAligner],
    client: Client,
    output: Pathish,
):
    with maybe_temp_directory() as tmpdir:
        structure_extension = ".pdb"
        reference_structure_path = tmpdir / f"{reference_name}{structure_extension}"
        target_structures_dir = tmpdir / "targets"

        logging.info("Saving structures to temporary directory")
        with Session(collection.get_engine(collection_db)) as session:
            reference_profile = collection.get_profile_from_name(session, reference_name)
            save_structure(reference_structure_path, reference_profile.structure)
            collection.export_structures(session, target_structures_dir, client)

        target_structures = {
            structure_name_and_extension(path)[0] | not_none: path
            for path in target_structures_dir.glob(f"*{structure_extension}")
        }

        # We are going to calculate a residue feature dataset for each method and
        # concatenate them along a dimension named "align_method". `datasets` will
        # hold the dataset for each method.
        datasets = []

        for method, aligner in aligners.items():
            logging.info(f"Running alignment with {method=}")

            datasets.append(
                create_feature_alignment(
                    aligner,
                    collection_db,
                    reference_structure_path,
                    target_structures,
                )
            )

            logging.info(f"Alignment dataset saved to {output}")

    combined_dataset = xr.concat(datasets, dim=pd.Index(aligners.keys(), name="align_method"))
    combined_dataset.to_netcdf(output)


@click.command()
@click.option(
    "-c",
    "--collection-db",
    required=True,
    type=click.Path(),
    help="Path to the collection database.",
)
@click.option(
    "-r",
    "--reference-name",
    required=True,
    type=str,
    help="Name of the reference structure.",
)
@click.option(
    "-o",
    "--output",
    required=True,
    type=click.Path(),
    help="Output NetCDF file.",
)
def main(
    collection_db: Pathish,
    reference_name: str,
    output: Pathish,
):
    with LocalCluster() as cluster, Client(cluster) as client:
        logging.info(f"Dask client: {client}")
        logging.info(f"View status at {client.dashboard_link}")

        preconfigured_aligners = get_preconfigured_aligners(client)
        run(collection_db, reference_name, preconfigured_aligners, client, output)


if __name__ == "__main__":
    main()
