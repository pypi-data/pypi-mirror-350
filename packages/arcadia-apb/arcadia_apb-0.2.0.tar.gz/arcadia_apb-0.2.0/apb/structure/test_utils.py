from pathlib import Path

import pytest

from apb._test_pointer import structure_paths
from apb.structure.convert import (
    load_structure,
    save_structure,
    structure_from_bytes,
    structure_to_bytes,
)
from apb.structure.utils import (
    RECOGNIZED_STRUCTURE_FILETYPES,
    extension_matches,
    find_structure_paths,
    structure_name_and_extension,
    structures_almost_equal,
)
from apb.utils import maybe_temp_directory

STRUCTURE_PATHS = structure_paths()


def test_structure_extension():
    # Base extensions work
    assert structure_name_and_extension("example.pdb") == ("example", ".pdb")
    assert structure_name_and_extension("example.cif") == ("example", ".cif")
    assert structure_name_and_extension("example.bcif") == ("example", ".bcif")

    # Supported compound extensions work
    assert structure_name_and_extension("example.pdb.gz") == ("example", ".pdb.gz")

    # Basenames with dots are OK
    assert structure_name_and_extension("example.0.pdb") == ("example.0", ".pdb")
    assert structure_name_and_extension("example.0.pdb.gz") == ("example.0", ".pdb.gz")
    assert structure_name_and_extension("example.0.cif") == ("example.0", ".cif")
    assert structure_name_and_extension("example.0.bcif") == ("example.0", ".bcif")

    # Diabolical cases don't take the bait
    assert structure_name_and_extension("example.pdb.gz.example") == (None, None)
    assert structure_name_and_extension("example.pdb.example") == (None, None)

    # Unsupported returns None tuple
    assert structure_name_and_extension("example") == (None, None)
    assert structure_name_and_extension("example.pdb.zip") == (None, None)
    assert structure_name_and_extension("example.bcif.gz") == (None, None)
    assert structure_name_and_extension("example.cif.gz") == (None, None)
    assert structure_name_and_extension("example.mmcif") == (None, None)


def test_find_structure_files():
    with maybe_temp_directory() as root:
        subdir1 = root / "subdir1"
        subdir1.mkdir()

        subdir2 = root / "subdir2"
        subdir2.mkdir()

        # Create structure files
        structure_file0 = subdir1 / "file1.pdb.gz"
        structure_file0.touch()
        structure_file1 = subdir1 / "file1.pdb"
        structure_file1.touch()
        structure_file2 = subdir1 / "file2.bcif"
        structure_file2.touch()
        structure_file3 = subdir2 / "fil.e3.cif"
        structure_file3.touch()

        # Unsupported structure file
        structure_file4 = root / "file4.cif.gz"
        structure_file4.touch()

        # Create non-structure files
        non_structure_file1 = subdir1 / "file5.txt"
        non_structure_file1.touch()
        non_structure_file2 = subdir2 / "file6.doc"
        non_structure_file2.touch()
        non_structure_file3 = root / "file7"
        non_structure_file3.touch()

        # Exhaust the generator, collecting the paths and the summary
        generator = find_structure_paths(root)
        structure_files: list[Path] = []
        try:
            while True:
                structure_files.append(next(generator))
        except StopIteration as e:
            summary = e.value

        # Structure files are in the result
        assert structure_file0 in structure_files
        assert structure_file1 in structure_files
        assert structure_file2 in structure_files
        assert structure_file3 in structure_files

        # Unsupported structure files are not
        assert structure_file4 not in structure_files

        # Non-structure files are not
        assert non_structure_file1 not in structure_files
        assert non_structure_file2 not in structure_files
        assert non_structure_file3 not in structure_files

        # The summary matches expectation
        assert summary.num_hits == 4
        assert summary.num_misses == 4
        assert summary.hit_exts == {".pdb", ".bcif", ".cif", ".pdb.gz"}
        assert summary.miss_exts == {".txt", ".doc", "", ".gz"}


@pytest.mark.parametrize("extension", RECOGNIZED_STRUCTURE_FILETYPES)
def test_extension_matches(extension: str):
    path = f"test_structure{extension}"

    # Default, which is all recognized structure filetypes, always matches
    assert extension_matches(path)

    # Matches if the extension is in `allowed`
    allowed = {".pdb.gz", ".cif"}
    assert extension_matches(path, allowed) == (extension in allowed)


@pytest.mark.parametrize("path", STRUCTURE_PATHS)
def test_structures_almost_equal(path: Path):
    # Load the structure
    structure = load_structure(path)

    # Structure almost equals its copy
    assert structures_almost_equal(structure, structure.copy())

    # Write, then read from various formats
    with maybe_temp_directory() as tmp_dir:
        base = tmp_dir / "protein"

        for ext in RECOGNIZED_STRUCTURE_FILETYPES:
            path = base.with_suffix(ext)
            save_structure(path, structure)

            assert structures_almost_equal(structure, load_structure(path))

    # Byte transformations also OK
    from_bytes = structure_from_bytes(structure_to_bytes(structure))
    assert structures_almost_equal(structure, from_bytes)

    # Changing coords yields False
    structure_copy = structure.copy()
    assert structure_copy.coord is not None
    structure_copy.coord[0] *= 1.0001
    assert not structures_almost_equal(structure, structure_copy)

    # Adding annotations yields False
    structure_copy = structure.copy()
    structure_copy.add_annotation("foo", dtype=bool)
    assert not structures_almost_equal(structure, structure_copy)

    # Setting annotations yields False
    structure_copy = structure.copy()
    structure_copy.set_annotation("bar", list(range(len(structure_copy))))
    assert not structures_almost_equal(structure, structure_copy)
