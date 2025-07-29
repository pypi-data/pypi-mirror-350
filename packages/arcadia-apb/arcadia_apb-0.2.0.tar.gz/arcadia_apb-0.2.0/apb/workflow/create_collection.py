from __future__ import annotations
import json
import logging
from pathlib import Path

import attrs
import cattrs
import click
import pandas as pd
from biotite.sequence.seqtypes import ProteinSequence
from biotite.structure.residues import get_residues
from dask.base import compute
from dask.delayed import Delayed, delayed
from dask.distributed import Client, LocalCluster
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

import apb.database.collection as collection
from apb.database.collection.interface import (
    add_preprocessed_profiles,
    get_all_protein_names,
    preprocess_profile,
)
from apb.profile import ProteinProfile
from apb.structure.convert import load_structure
from apb.structure.features.accessibility import calc_solvent_accessibility
from apb.structure.features.accessibility.datatypes import MaxSASASource, SolventAccessibilityConfig
from apb.structure.features.secondary_structure import calc_3_state_secondary_structure
from apb.structure.utils import find_structure_paths, structure_name_and_extension
from apb.types import Pathish, not_none
from apb.utils import converter

BATCH_SIZE: int = 1000


def save_feature_config(config: FeatureCalculationConfig, path: Pathish) -> Path:
    """Save a FeatureRecipe to file

    Note:
        - This function is not a method of `FeatureCalculationConfig` due to Dask
          parallelization requirements. Dask needs all involved objects to be
          serializable, and `FeatureCalculationConfig` is one of those objects.
          Instances of `FeatureCalculationConfig` can be converted to JSON using a
          cattrs `converter` object, as shown in this function. However, Dask
          serializes not just the instances but also the class itself. This poses a
          problem because the `converter` object is not easily serializable.

          If any methods in `FeatureCalculationConfig` reference the `converter` object,
          the class becomes non-serializable. The following attempts to serialize the
          `converter` object with Dask were unsuccessful:

            - Registering a cloudpickle patch for lru_cache objects, which led to
              downstream pickle issues.
              (https://github.com/cloudpipe/cloudpickle/issues/178#issuecomment-975735397)

            - Implementing a dill serialization family for Dask, which allowed the
              converter to be serialized but resulted in a 'TypeError: cannot pickle
              'KeyedRef' object'.
              (https://distributed.dask.org/en/stable/serialization.html)
    """
    with open(path, "w") as fp:
        json.dump(converter.unstructure(config), fp, indent=2)

    return Path(path)


def load_feature_config(path: Pathish) -> FeatureCalculationConfig:
    """Load a FeatureRecipe JSON from file

    Note:
        - See `save_feature_config` notes
    """
    with open(path) as fp:
        payload = json.load(fp)
        try:
            return converter.structure(payload, FeatureCalculationConfig)
        except cattrs.errors.ClassValidationError as e:
            user_message = (
                "The JSON file could not be structured as a feature config. Please "
                "check the input data and try again."
            )
            raise ValueError(user_message) from e


@attrs.define
class FeatureCalculationConfig:
    """Config that describes protein feature specifications

    This class holds all the tunables for calculating features like solvent
    accessibility, etc.

    Attributes:
        rsa_config: Configuration for relative solvent accessibility.
        sasa_config: Configuration for solvent accessible surface area.
    """

    rsa_config: SolventAccessibilityConfig
    sasa_config: SolventAccessibilityConfig

    @classmethod
    def default(cls) -> FeatureCalculationConfig:
        return cls(
            rsa_config=SolventAccessibilityConfig(
                normalize=True,
                source=MaxSASASource.WILKE,
                point_number=300,
            ),
            sasa_config=SolventAccessibilityConfig(
                normalize=False,
                source=MaxSASASource.WILKE,
                point_number=300,
            ),
        )


def _compute_and_insert(
    client: Client,
    engine: Engine,
    profiling_tasks: list[Delayed],
    batch_count: int,
) -> None:
    # Execute the profiling tasks in parallel
    profiles = compute(*profiling_tasks, scheduler=client)

    # Insert them (synchronously)
    with Session(engine) as session:
        add_preprocessed_profiles(session, profiles)

    logging.info(f"{BATCH_SIZE * batch_count + len(profiles)} profiles processed")


def build_profile(structure_path: Path, config: FeatureCalculationConfig) -> ProteinProfile:
    structure = load_structure(structure_path)
    sequence = ProteinSequence(get_residues(structure)[1])

    name = structure_name_and_extension(structure_path)[0] | not_none

    return ProteinProfile(
        name=name,
        sequence=sequence,
        structure=structure,
        residue_features=pd.DataFrame(
            {
                collection.Residue.secondary_structure.key: calc_3_state_secondary_structure(
                    structure
                ),
                collection.Residue.solvent_accessibility.key: calc_solvent_accessibility(
                    structure, config.sasa_config
                ),
                collection.Residue.relative_solvent_accessibility.key: calc_solvent_accessibility(
                    structure, config.rsa_config
                ),
            }
        ),
    )


def main(
    structure_dir: Pathish,
    db_path: Pathish,
    config: FeatureCalculationConfig,
    client: Client,
    batch_size: int = BATCH_SIZE,
) -> None:
    """Process structure files and add them to a ProteinDB.

    Args:
        directory: The directory containing structure files.
        db_path: Path to the database file.
        config: A feature config that is used to calculate features.
        batch_size:
            The DB is written in batches of protein profiles. This parameter controls
            the number of protein profiles held in the batch cache before they are
            inserted into the DB and released from memory.
    """
    logging.info(f"Using run config: {config}")

    engine = collection.get_engine(db_path, create=True)

    with Session(engine) as session:
        names = set(get_all_protein_names(session))

    profiling_tasks: list[Delayed] = []

    batch_count = 0
    duplicate_names = set()
    for structure_path in find_structure_paths(structure_dir):
        name = structure_name_and_extension(structure_path)[0] | not_none

        if name in names:
            # Skip proteins with names that have already been processed
            duplicate_names.add(name)
            continue

        profile_task = delayed(build_profile)(structure_path, config)
        preprocess_task = delayed(preprocess_profile)(profile_task)
        profiling_tasks.append(preprocess_task)

        names.add(name)

        if len(profiling_tasks) >= batch_size:
            _compute_and_insert(client, engine, profiling_tasks, batch_count)
            profiling_tasks.clear()

            batch_count += 1

    # Handle remaining tasks
    _compute_and_insert(client, engine, profiling_tasks, batch_count)
    profiling_tasks.clear()

    if len(duplicate_names):
        duplicate_list = list(duplicate_names)
        display_limit = min(len(duplicate_list), 100)
        logging.info(
            f"There were {len(duplicate_names)} duplicate proteins that were skipped. Here are "
            f"the first {display_limit}: {duplicate_list[:display_limit]}"
        )


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx: click.Context) -> None:
    """Create a protein collection database

    A prototype CLI for creating a protein database that stores the underlying sequence,
    structure, residue features, and paired residue features for each entry.
    """
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@cli.command()
@click.argument("path", type=click.Path())
def config(path: Path):
    """Create a feature config file and exit.

    This is useful if you want to control what features are calculated and how. FIXME
    this is mostly a placeholder for future development.
    """
    path = Path(path)
    if path.exists():
        raise FileExistsError(f"{path} already exists. Won't overwrite")

    save_feature_config(FeatureCalculationConfig.default(), path)
    click.echo(f"Feature config file created at {path}")


@cli.command()
@click.option(
    "-i",
    "--input",
    required=True,
    type=click.Path(exists=True),
    help="Directory containing structure files.",
)
@click.option(
    "-o",
    "--output",
    required=True,
    type=click.Path(),
    help="Path to the database file.",
)
@click.option(
    "-c",
    "--feature-config",
    required=False,
    type=click.Path(),
    help=(
        "Path to the configurable config file. Default will be used if not provided. Use `config` "
        "subcommand to generate a config file to use."
    ),
)
def run(input: Path, output: Path, feature_config: Path):
    """Load and process protein structures into a database."""
    config = (
        load_feature_config(feature_config)
        if feature_config
        else FeatureCalculationConfig.default()
    )
    with LocalCluster() as cluster, Client(cluster) as client:
        logging.info(f"Dask client: {client}")
        logging.info(f"View status at {client.dashboard_link}")
        main(input, output, config, client)


if __name__ == "__main__":
    cli()
