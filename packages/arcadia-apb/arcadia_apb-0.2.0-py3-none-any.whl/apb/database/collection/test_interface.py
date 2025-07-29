from collections.abc import Iterator
from pathlib import Path

import attrs
import numpy as np
import pandas as pd
import pytest
from biotite.sequence.seqtypes import ProteinSequence
from biotite.structure.residues import get_residues
from dask.distributed import Client, LocalCluster
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists

import apb.database.collection as collection
from apb._test_pointer import structure_paths
from apb.database.collection.interface import (
    export_structures,
    iter_all_profiles,
    load_all_profiles,
)
from apb.database.collection.schema import Residue, residue_dataframe_schema
from apb.database.utils import DB_SCHEME, path_to_uri
from apb.profile import ProteinProfile
from apb.structure.convert import load_structure
from apb.structure.features.accessibility import calc_solvent_accessibility
from apb.structure.features.accessibility.datatypes import SolventAccessibilityConfig
from apb.structure.features.secondary_structure import calc_3_state_secondary_structure
from apb.structure.utils import (
    RECOGNIZED_STRUCTURE_FILETYPES,
    structure_name_and_extension,
    structures_almost_equal,
)
from apb.types import not_none
from apb.utils import maybe_temp_directory


@pytest.fixture
def db(tmp_path):
    return collection.get_engine(tmp_path / "test.db", create=True)


@pytest.fixture
def profiles() -> list[ProteinProfile]:
    profiles: list[ProteinProfile] = []

    for path in structure_paths():
        structure = load_structure(path)
        name = structure_name_and_extension(path)[0] | not_none
        sequence = ProteinSequence(get_residues(structure)[1])

        rsa_config = attrs.evolve(SolventAccessibilityConfig.default(), normalize=True)
        sasa_config = attrs.evolve(SolventAccessibilityConfig.default(), normalize=False)

        res_features = pd.DataFrame(
            {
                Residue.secondary_structure.key: calc_3_state_secondary_structure(structure),
                Residue.solvent_accessibility.key: calc_solvent_accessibility(
                    structure, sasa_config
                ),
                Residue.relative_solvent_accessibility.key: calc_solvent_accessibility(
                    structure, rsa_config
                ),
            }
        )

        # When features don't have a value for each residue, their missing values in the
        # `ProteinProfile.residue_features` are cast as null values. It's imperative
        # that missing data maintain datatype consistency as they are written to and
        # subsequently read from a collection DB. This is simulated by randomly setting
        # 10 of any nullable feature's values to null.
        for feature_name in res_features.columns:
            if residue_dataframe_schema.columns[feature_name].nullable:
                indices_to_null = np.random.choice(res_features.shape[0], 10, replace=False)
                res_features.loc[indices_to_null, feature_name] = None

        profiles.append(
            ProteinProfile(
                name=name,
                sequence=sequence,
                structure=structure,
                residue_features=res_features,
            )
        )

    return profiles


def test_load_db(tmp_path: Path):
    # This DB doesn't exist
    db_path = tmp_path / "test.db"
    assert not db_path.exists()
    assert not database_exists(path_to_uri(db_path))

    # Problem loading non-existant DB
    with pytest.raises(ValueError):
        return collection.get_engine(db_path, create=False)

    # It still doesn't exist (no side effects from the call)
    assert not db_path.exists()
    assert not database_exists(path_to_uri(db_path))

    # No problem if create is set to True
    collection.get_engine(db_path, create=True)

    # Now it exists
    assert db_path.exists()
    assert database_exists(path_to_uri(db_path))


def test_get_profile(db: Engine, profiles: list[ProteinProfile]):
    profile = profiles[0]

    # Fetching profile from empty DB doesn't work
    with Session(db) as session:
        with pytest.raises(KeyError, match="is not present"):
            collection.get_profile_from_index(session, 1)

    with Session(db) as session:
        with pytest.raises(KeyError, match="is not present"):
            collection.get_profile_from_name(session, profile.name)

    # Write the profile to the DB
    with Session(db) as session:
        collection.add_profiles(session, (profile,))

    # Fetching profile using non-existant keys doesn't work.
    with Session(db) as session:
        with pytest.raises(KeyError, match="is not present"):
            collection.get_profile_from_index(session, 2)

    with Session(db) as session:
        with pytest.raises(KeyError, match="is not present"):
            collection.get_profile_from_name(session, "foo")

    # Fetching the profile with the correct keys works
    with Session(db) as session:
        collection.get_profile_from_index(session, 1)

    with Session(db) as session:
        collection.get_profile_from_name(session, profile.name)


def _assert_profiles_equal(profile: ProteinProfile, other: ProteinProfile) -> None:
    assert isinstance(profile, ProteinProfile)
    assert isinstance(other, ProteinProfile)
    assert profile.name == other.name
    assert structures_almost_equal(profile.structure, other.structure)
    assert profile.sequence == other.sequence
    assert other.residue_features.equals(profile.residue_features)
    assert (other.residue_features.dtypes == profile.residue_features.dtypes).all()


def test_get_profile_from_name(db: Engine, profiles: list[ProteinProfile]):
    # Write the profiles to the DB
    with Session(db) as session:
        collection.add_profiles(session, profiles)

    for profile in profiles:
        # Build the profile from the DB
        with Session(db) as session:
            profile_from_db = collection.get_profile_from_name(session, profile.name)

        # They are the same
        _assert_profiles_equal(profile, profile_from_db)


def test_iter_all_profiles(db: Engine, profiles: list[ProteinProfile]):
    # Write the profiles to the DB
    with Session(db) as session:
        collection.add_profiles(session, profiles)

    with Session(db) as session:
        profile_iterator = iter_all_profiles(session)

    assert isinstance(profile_iterator, Iterator)

    # For each profile generated from the iterator, assert that it equates with the
    # corresponding profile. Note that the zip tests that order is maintained.
    for profile, profile_from_db in zip(profiles, profile_iterator, strict=True):
        _assert_profiles_equal(profile, profile_from_db)


def test_load_all_profiles(db: Engine, profiles: list[ProteinProfile]):
    # Write the profiles to the DB
    with Session(db) as session:
        collection.add_profiles(session, profiles)

    db_path = str(db.url).replace(DB_SCHEME, "")
    profiles_from_db = load_all_profiles(db_path)
    assert isinstance(profiles_from_db, list)

    # For each profile in the load_all_profiles result, assert that it equates with the
    # corresponding profile. Note that the zip tests that order is maintained.
    for profile, profile_from_db in zip(profiles, profiles_from_db, strict=True):
        _assert_profiles_equal(profile, profile_from_db)


@pytest.mark.parametrize("extension", RECOGNIZED_STRUCTURE_FILETYPES)
def test_export_structures(
    db: Engine, profiles: list[ProteinProfile], extension: str, cluster: LocalCluster
):
    with Session(db) as session:
        collection.add_profiles(session, profiles)

        # Store the exported structures, then load them from file
        with maybe_temp_directory() as tmpdir:
            with Client(cluster) as client:
                export_structures(session, tmpdir, extension=extension, client=client)

            loaded_structures = {
                structure_name_and_extension(path)[0]: load_structure(path)
                for path in tmpdir.glob(f"*{extension}")
            }

    # Now assert each profile structure matches the structure loaded from file
    for profile in profiles:
        assert structures_almost_equal(profile.structure, loaded_structures[profile.name])
