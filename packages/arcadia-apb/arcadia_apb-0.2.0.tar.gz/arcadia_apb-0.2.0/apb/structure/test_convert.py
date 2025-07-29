from pathlib import Path

import pytest

from apb._test_pointer import structure_paths
from apb.structure.convert import (
    load_structure,
    save_structure,
    structure_from_bytes,
    structure_to_bytes,
)
from apb.structure.utils import structures_almost_equal
from apb.types import ProteinStructure
from apb.utils import maybe_temp_directory

STRUCTURE_PATHS = structure_paths()
EXTENSIONS = [".pdb", ".pdb.gz", ".cif", ".bcif"]


@pytest.fixture
def structure() -> ProteinStructure:
    return load_structure(STRUCTURE_PATHS[0])


@pytest.mark.parametrize("path", STRUCTURE_PATHS)
def test_byte_round_trip(path: Path):
    # Load a structure
    structure = load_structure(path)

    # Represent it as bytes
    as_bytes = structure_to_bytes(structure)
    assert isinstance(as_bytes, bytes)

    # Now read it from bytes
    from_bytes = structure_from_bytes(as_bytes)

    # Besides floating point imprecision, it's an isomorphic round trip
    assert structures_almost_equal(structure, from_bytes)


@pytest.mark.parametrize("extension", EXTENSIONS)
def test_save_load_roundtrip(structure: ProteinStructure, extension: str):
    with maybe_temp_directory() as tmp_dir:
        path = tmp_dir / f"test{extension}"

        # Save the structure
        save_structure(path, structure)

        # It is in the file system
        assert path.exists()

        # Now load it
        structure_from_file = load_structure(path)

        # It equates
        assert structures_almost_equal(structure, structure_from_file)
