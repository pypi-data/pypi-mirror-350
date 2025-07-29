import pandas as pd
import pytest
from biotite.sequence.seqtypes import ProteinSequence
from biotite.structure.residues import get_residues

from apb._test_pointer import structure_paths
from apb.structure.convert import load_structure
from apb.structure.features.secondary_structure import calc_3_state_secondary_structure, ss3_dtype

STRUCTURE_PATHS = structure_paths()


@pytest.mark.parametrize("path", STRUCTURE_PATHS)
def test_calc_ss_output(path):
    structure = load_structure(path)
    sequence = ProteinSequence(get_residues(structure)[1])
    out = calc_3_state_secondary_structure(structure)

    # Dtype is right
    assert out.dtype == ss3_dtype, "Values should be categorical dtype"

    # Name is correct
    assert out.name == "secondary_structure"

    # Length matches sequence
    assert len(sequence) == len(out)

    # There are no null values
    assert not out.isnull().any()

    # Assert indices are properly ordered and start at 0
    assert out.index.equals(pd.Index(range(len(sequence))))
