from itertools import combinations

import attrs
import numpy as np
import pandas as pd
import pytest
from biotite.sequence.seqtypes import ProteinSequence
from biotite.structure.residues import get_residues

from apb._test_pointer import structure_paths
from apb.structure.convert import load_structure
from apb.structure.features.accessibility import calc_solvent_accessibility
from apb.structure.features.accessibility.datatypes import MaxSASASource, SolventAccessibilityConfig

STRUCTURE_PATHS = structure_paths()
SASA_SOURCES = [source for source in MaxSASASource]

TEST_CONFIG = SolventAccessibilityConfig.default()


@pytest.mark.parametrize("path", STRUCTURE_PATHS)
@pytest.mark.parametrize("source", MaxSASASource)
def test_output(path, source):
    structure = load_structure(path)
    sequence = ProteinSequence(get_residues(structure)[1])
    config = attrs.evolve(TEST_CONFIG, source=source, normalize=True)
    out = calc_solvent_accessibility(structure, config)

    # Dtype is right
    assert out.dtype == "float64", "Values should be categorical dtype"

    # Name is correct
    assert out.name == "relative_solvent_accessibility"

    # Length matches sequence
    assert len(sequence) == len(out)

    # There are no null values
    assert not out.isnull().any()

    # Assert indices are properly ordered and start at 0
    assert out.index.equals(pd.Index(range(len(sequence))))


@pytest.mark.parametrize("path", STRUCTURE_PATHS)
@pytest.mark.parametrize("source", MaxSASASource)
def test_normalize(path, source):
    structure = load_structure(path)

    # Make a config with the specified source
    config = attrs.evolve(TEST_CONFIG, source=source, normalize=True)

    out = calc_solvent_accessibility(structure, config)

    # Range is between 0 and 1
    assert (out <= 1.0).all()
    assert (out >= 0).all()

    # Name is relative_solvent_accessibility
    assert out.name == "relative_solvent_accessibility"

    # Make an unnormalized config
    config = attrs.evolve(TEST_CONFIG, source=source, normalize=False)

    out = calc_solvent_accessibility(structure, config)

    # Values exceed 1.0
    assert (out > 1.0).any()
    assert (out >= 0).all()

    # Name is solvent_accessibility
    assert out.name == "solvent_accessibility"


@pytest.mark.parametrize("path", STRUCTURE_PATHS)
def test_sources(path):
    config = TEST_CONFIG
    structure = load_structure(path)

    outs = {}

    for source in MaxSASASource:
        # Make a config with the specified source
        config = attrs.evolve(TEST_CONFIG, source=source, normalize=True)

        outs[source] = calc_solvent_accessibility(structure, config).values

    # Ensure all outputs are different
    for source1, source2 in combinations(outs.keys(), 2):
        assert not np.array_equal(outs[source1], outs[source2]), (
            f"Outputs for sources {source1} and {source2} should not be identical"
        )
