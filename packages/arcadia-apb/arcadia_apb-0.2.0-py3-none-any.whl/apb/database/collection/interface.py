"""Protein collection database management

This module provides functionality for adding protein profiles to a 'collection'
database and retrieving the contents. It handles the conversion of protein structures to
and from byte format for database storage and ensures the integrity of residue feature
data using pandera.
"""

from __future__ import annotations
import logging
from collections.abc import Generator, Iterable
from pathlib import Path
from typing import Any

import pandas as pd
from biotite.sequence.seqtypes import ProteinSequence
from dask.base import compute
from dask.delayed import Delayed, delayed
from dask.distributed import Client
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists

import apb.database.collection.schema as collection_schema
from apb.database.utils import create_db, engine_from_path, engine_from_session, path_to_uri
from apb.profile import ProteinProfile
from apb.structure.convert import (
    save_structure,
    structure_from_bytes,
    structure_to_bytes,
)
from apb.structure.utils import RECOGNIZED_STRUCTURE_FILETYPES
from apb.types import Pathish

logging.getLogger("distributed").setLevel(logging.WARNING)
logging.getLogger("dask").setLevel(logging.WARNING)


PreprocessProfileReturnType = tuple[collection_schema.Protein, pd.DataFrame]


def load_all_profiles(path: Pathish) -> list[ProteinProfile]:
    """Loads and returns all protein profiles from a specified database.

    This function simplifies the process of retrieving protein profiles from a database
    by creating an internally managed SQLAlchemy session. By providing the path to the
    database, users can easily access all protein profiles without needing to manually
    handle session creation and management. This function is especially useful for users
    who frequently need to access protein profiles and want/need a straightforward
    method to do so.

    Args:
        path: The filesystem path or similar reference to the database.

    Returns:
        list[ProteinProfile]: A list of all protein profiles contained in the database.

    See Also:
        - iter_all_profiles: Function called internally to retrieve profiles.
    """
    with Session(get_engine(path, create=False)) as session:
        return list(iter_all_profiles(session))


def get_engine(path: Pathish, create: bool = False) -> Engine:
    """Load a SQLAlchemy engine for a protein collection

    Args:
        path:
            The file system path to the database. This should be convertible to a URI.
        create:
            Flag indicating whether to create the database if it does not exist.
            Defaults to `False`. If the path doesn't resolve to a DB and this is False,
            a ValueError is raised.

    Returns:
        Engine:
            A SQLAlchemy Engine instance connected to the specified database.

    Raises:
        ValueError: If the database does not exist and `create` is set to `False`.
    """
    uri = path_to_uri(path)
    engine = engine_from_path(path)

    if database_exists(uri):
        return engine

    if not create:
        raise ValueError(f"{path} doesn't exist")

    create_db(engine, collection_schema.Base, exist_ok=False)
    return engine


def add_profiles(session: Session, profiles: Iterable[ProteinProfile]) -> None:
    """Add profiles to the database

    Args:
        profiles:
            Iterable of protein profiles
    """
    add_preprocessed_profiles(session, (preprocess_profile(profile) for profile in profiles))


def add_preprocessed_profiles(
    session: Session, preprocessed_profiles: Iterable[PreprocessProfileReturnType]
) -> None:
    """Add preprocessed profiles to the database

    "Preprocessed profiles" are the return type of `preprocess_profile`.

    Args:
        profiles:
            An iterable of tuples where each tuple contains a Protein entry and a
            residue DataFrame.
    """
    residue_dfs: list[pd.DataFrame] = []

    for protein_entry, residue_df in preprocessed_profiles:
        session.add(protein_entry)
        session.flush()

        residue_df["protein_id"] = protein_entry.id
        residue_dfs.append(residue_df)

    if not len(residue_dfs):
        return

    # Validate the concatenated dataframe
    all_protein_residue_df = collection_schema.residue_dataframe_schema.validate(
        pd.concat(residue_dfs, ignore_index=True)
    )

    # Bulk insert the residue entries
    session.bulk_insert_mappings(
        collection_schema.Residue,  # type: ignore
        all_protein_residue_df.to_dict(orient="records"),
    )

    session.commit()


def preprocess_profile(profile: ProteinProfile) -> tuple[collection_schema.Protein, pd.DataFrame]:
    """Decompose a profile's data into table components prior to database insertion

    Returns:
        collection_schema.Protein:
            A collection_schema.Protein object.
        pd.DataFrame:
            The profile's residue features dataframe.
    """
    protein_entry = collection_schema.Protein(
        name=profile.name,
        sequence=str(profile.sequence),
        structure=structure_to_bytes(profile.structure),
        source=profile.source,
    )

    residue_df = profile.residue_features.reset_index()

    return protein_entry, residue_df


def _get_protein_by(session: Session, **kwargs: Any) -> collection_schema.Protein:
    """Helper function to retrieve a protein by given keyword arguments"""
    engine = engine_from_session(session)
    protein = session.query(collection_schema.Protein).filter_by(**kwargs).one_or_none()

    if protein is None:
        raise KeyError(f"Protein with {kwargs} is not present in {engine.url}.")

    return protein


def _build_protein_profile(session: Session, protein: collection_schema.Protein) -> ProteinProfile:
    """Helper function to build a ProteinProfile from a Protein SQLAlchemy object."""
    engine = engine_from_session(session)
    sequence = ProteinSequence(protein.sequence)
    structure = structure_from_bytes(protein.structure)  # type: ignore

    statement = session.query(collection_schema.Residue).filter_by(protein_id=protein.id).statement

    return ProteinProfile(
        name=str(protein.name),
        sequence=sequence,
        structure=structure,
        residue_features=(
            pd.read_sql(statement, engine)
            .pipe(collection_schema.residue_dataframe_schema.validate)
            .drop(["id", "protein_id", "residue_index"], axis=1)
        ),
        source=str(protein.source),
    )


def get_profile_from_index(session: Session, protein_id: int) -> ProteinProfile:
    protein = _get_protein_by(session, id=protein_id)
    return _build_protein_profile(session, protein)


def get_profile_from_name(session: Session, protein_name: str) -> ProteinProfile:
    protein = _get_protein_by(session, name=protein_name)
    return _build_protein_profile(session, protein)


def export_structures(
    session: Session,
    structure_dir: Pathish,
    client: Client,
    extension: str = ".pdb",
) -> Path:
    """Exports structures into a directory"""
    if extension not in RECOGNIZED_STRUCTURE_FILETYPES:
        raise ValueError(
            f"Unknown extension '{extension}'. Allowed extensions: {RECOGNIZED_STRUCTURE_FILETYPES}"
        )

    structure_dir = Path(structure_dir)
    if not structure_dir.exists():
        structure_dir.mkdir(parents=True)

    # Ideally, the input to a dask delayed chain is something simple like an integer or
    # the path to a file. This is because the object is a part of the DAG. Yet in this
    # case, the input to the structure is the protein SQLAlchemy object. This limits the
    # size we can make the task graph before running out of memory. I chose 5000 because
    # this creates a graph size <1Gb.
    batch_size = 5000

    save_tasks: list[Delayed] = []
    for protein in session.query(collection_schema.Protein).yield_per(batch_size):
        structure = delayed(structure_from_bytes)(protein.structure)
        save_task = delayed(save_structure)(structure_dir / f"{protein.name}{extension}", structure)
        save_tasks.append(save_task)

        if len(save_tasks) >= batch_size:
            compute(*save_tasks, scheduler=client)
            save_tasks = []

    if len(save_tasks):
        compute(*save_tasks, scheduler=client)

    return structure_dir


def iter_all_profiles(session: Session) -> Generator[ProteinProfile, None, None]:
    """Returns an iterator of all profiles in the DB

    This function iterates through all protein names in the database, and yields a
    protein profile for each one by querying the database based on the protein name. The
    function uses a generator, making it memory efficient for large datasets as it
    yields profiles one at a time.

    Examples:
        To load all profiles into memory, you can convert the generator to a list:

        >>> profiles = list(get_all_profiles(session))

        To iteratively print the length of each protein sequence:

        >>> for profile in get_all_profiles(session):
        >>>     print(f"{profile.name}: Sequence Length = {len(profile.sequence)}")

    See Also:
        - `load_all_profiles`
    """
    for name in get_all_protein_names(session):
        yield get_profile_from_name(session, name)


def get_all_protein_names(session: Session) -> list[str]:
    return [name for name, *_ in session.query(collection_schema.Protein.name).all()]
