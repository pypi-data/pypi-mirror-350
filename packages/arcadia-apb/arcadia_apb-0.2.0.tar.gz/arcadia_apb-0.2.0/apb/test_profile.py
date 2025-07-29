import numpy as np
import pandas as pd
import pytest
from biotite.sequence.seqtypes import ProteinSequence
from biotite.structure.residues import get_residues

from apb._test_pointer import structure_paths
from apb.profile import ProteinProfile, get_residue_index
from apb.structure.convert import load_structure
from apb.types import ProteinStructure

STRUCTURE_PATH = structure_paths()[0]

np.random.seed(42)


@pytest.fixture
def structure() -> ProteinStructure:
    return load_structure(STRUCTURE_PATH)


@pytest.fixture
def sequence(structure: ProteinStructure) -> ProteinSequence:
    _, residues = get_residues(structure)
    return ProteinSequence(residues)


def _diverse_res_features(N: int) -> pd.DataFrame:
    int_series = pd.Series(np.random.randint(1, 100, size=N), name="Integer")
    float_series = pd.Series(np.random.random(N), name="Float")
    str_series = pd.Series([f"Item_{i}" for i in range(N)], name="String")
    bool_series = pd.Series(np.random.choice([True, False], size=N), name="Boolean")
    categorical_series = pd.Series(
        pd.Categorical(["c1", "c2", "3"][i % 3] for i in range(N)),
        name="Category",
    )

    return pd.DataFrame(
        {
            int_series.name: int_series,
            float_series.name: float_series,
            str_series.name: str_series,
            bool_series.name: bool_series,
            categorical_series.name: categorical_series,
        }
    )


def test_no_res_features(structure, sequence):
    # Create a featureless profile
    profile = ProteinProfile("test_profile", sequence, structure)

    # The amino acid column was absent, so it was added and equals the sequence
    assert "amino_acid" in profile.residue_features.columns
    assert "".join(sequence.symbols.tolist()) == "".join(
        profile.residue_features["amino_acid"].tolist()
    )

    # It has the proper index
    assert len(profile.residue_features.index) == len(sequence)
    assert profile.residue_features.index.equals(pd.Index(range(len(sequence))))


def test_yes_res_features(structure, sequence):
    res_features = _diverse_res_features(len(sequence))
    expected_index = get_residue_index(len(sequence))

    # The indices match so there's no problem
    assert res_features.index.equals(expected_index)
    profile = ProteinProfile("test_profile", sequence, structure, res_features)

    # The res_features frame _is_ the passed frame
    assert profile.residue_features is res_features

    # The amino acid column was absent, so it was added and equals the sequence
    assert "amino_acid" in profile.residue_features.columns
    assert "".join(sequence.symbols.tolist()) == "".join(
        profile.residue_features["amino_acid"].tolist()
    )

    # When the indices don't match, problem
    res_features.index = res_features.index.astype(str)
    assert not res_features.index.equals(expected_index)
    with pytest.raises(ValueError, match="Dataframe indices don't match expectation"):
        ProteinProfile("test_profile", sequence, structure, res_features)


def test_add_feature(structure, sequence):
    # Create a featureless profile
    profile = ProteinProfile("test_profile", sequence, structure)

    # Feature must be named
    with pytest.raises(ValueError, match="Unnamed series feature."):
        profile.add_feature(pd.Series(np.random.rand(len(sequence))))

    # Feature must have right length
    with pytest.raises(ValueError, match="must match sequence length"):
        profile.add_feature(pd.Series(np.random.rand(len(sequence) - 1), name="f1"))

    # Feature indices must match!
    with pytest.raises(ValueError, match="Dataframe indices don't match expectation"):
        feature = pd.Series(np.random.rand(len(sequence)), name="f1")
        feature.index += 1
        profile.add_feature(feature)

    # Signed 64-bit integer dtype is not the expected index
    feature = pd.Series(np.random.rand(len(sequence)), name="f1")
    feature.index = feature.index.astype(np.int64)
    assert feature.index.dtype != profile.residue_features.index.dtype

    # But datatypes can be coerced without altering res_features index
    index_before = profile.residue_features.index.copy(deep=True)
    profile.add_feature(feature)
    assert str(profile.residue_features.index.dtype) == str(index_before.dtype) == "uint32"
    assert not profile.residue_features[feature.name].isnull().any()  # type: ignore

    # Cannot add existing feature name
    with pytest.raises(ValueError, match="already present"):
        profile.add_feature(feature)
