from pathlib import Path

import pytest
from biotite.structure.residues import get_residues
from dask.distributed import Client, LocalCluster

from apb._test_pointer import TEST_RAW_COLLECTION
from apb.application.tmalign.align import (
    align_many_to_many,
    align_to_reference,
    load_alignments_json,
    save_alignments_json,
)
from apb.structure.convert import load_structure, save_structure
from apb.structure.utils import structure_name_and_extension
from apb.types import not_none

QUERY_STRUCTURE_COUNT = 3
TARGET_STRUCTURE_COUNT = 4


@pytest.fixture
def target_structures(tmpdir: Path) -> dict[str, Path]:
    output: dict[str, Path] = {}

    for count, path in enumerate(TEST_RAW_COLLECTION.glob("*")):
        if count == TARGET_STRUCTURE_COUNT:
            break

        name, ext = structure_name_and_extension(path)

        if ext == ".pdb":
            pdb_path = path
        else:
            pdb_path = tmpdir / f"{name}.pdb"
            save_structure(pdb_path, load_structure(path))

        output[not_none(name)] = pdb_path

    return output


@pytest.fixture
def query_structures(target_structures: dict[str, Path]) -> dict[str, Path]:
    output: dict[str, Path] = {}

    for count, (target, structure) in enumerate(target_structures.items()):
        if count == QUERY_STRUCTURE_COUNT:
            break

        output[target] = structure

    return output


@pytest.fixture
def reference_structure(target_structures: dict[str, Path]) -> Path:
    return list(target_structures.values())[0]


@pytest.fixture
def structure_path_with_bad_extension(reference_structure: Path) -> Path:
    return Path(reference_structure).with_suffix(".pdb.gz")


def test_align_many_to_many(
    query_structures: dict[str, Path],
    target_structures: dict[str, Path],
    tmpdir: Path,
    cluster: LocalCluster,
):
    with Client(cluster) as client:
        output = align_many_to_many(query_structures, target_structures, client)

    expected_length = len(query_structures) * len(target_structures)

    length = 0
    for query in output:
        length += len(output[query])

        for target in output[query]:
            # Every entry is populated.
            assert output[query][target] is not None

            # Assert inverse relationship where applicable
            if target in output and query in output[target]:
                alignment = output[query][target]
                inverse = output[target][query]
                assert alignment.qseq_aligned == inverse.tseq_aligned
                assert alignment.tseq_aligned == inverse.qseq_aligned
                assert alignment.ttmscore == inverse.qtmscore
                assert alignment.qtmscore == inverse.ttmscore
                assert alignment.aligned == inverse.aligned
                assert alignment.rmsd == inverse.rmsd

    assert length == expected_length

    # Test round trip serialization
    assert output == load_alignments_json(save_alignments_json(tmpdir / "data.json", output))


def test_align_to_reference(
    reference_structure: Path, target_structures: dict[str, Path], cluster: LocalCluster
):
    with Client(cluster) as client:
        result = align_to_reference(reference_structure, target_structures, client)

    # The index length matches the reference length
    ref_length = len(get_residues(load_structure(reference_structure))[1])
    assert len(result.index) == ref_length


def test_align_to_ref_fail_if_bad_extension(
    structure_path_with_bad_extension: Path,
    target_structures: dict[str, Path],
    cluster: LocalCluster,
):
    with Client(cluster) as client:
        with pytest.raises(ValueError, match="TMalign only accepts the extensions:"):
            align_to_reference(structure_path_with_bad_extension, target_structures, client)
