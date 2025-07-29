from pathlib import Path

import numpy as np
import pytest

from apb._test_pointer import TEST_RAW_COLLECTION
from apb.application.foldseek.align import (
    CIGAR_OUTPUT_FORMAT,
    DEFAULT_REFERENCE_ALIGNMENT_CONVERTALIS_CONFIG,
    DEFAULT_REFERENCE_ALIGNMENT_SEARCH_CONFIG,
    _ensure_valid_search_config,
    _generate_cigar_strings,
    align_to_reference,
)
from apb.application.foldseek.base import createdb
from apb.application.foldseek.datatypes import FoldSeekSearchConfig
from apb.application.foldseek.utils import create_tsv_for_createdb
from apb.structure.utils import structure_name_and_extension
from apb.types import not_none
from apb.utils import maybe_temp_directory


@pytest.fixture
def db(tmp_path: Path) -> Path:
    return createdb(TEST_RAW_COLLECTION, tmp_path / "output_db")


@pytest.fixture
def reference_path() -> Path:
    return TEST_RAW_COLLECTION / "A0A0A7RVV1.pdb.gz"


@pytest.fixture
def target_structures() -> dict[str, Path]:
    targets = {}
    for path in sorted(list(TEST_RAW_COLLECTION.glob("*"))):
        name = structure_name_and_extension(path)[0] | not_none
        targets[name] = path

    return targets


def test_ensure_valid_search_config():
    valid_config = FoldSeekSearchConfig(backtrace=True)
    _ensure_valid_search_config(valid_config)

    invalid_config = FoldSeekSearchConfig(backtrace=False)
    with pytest.raises(ValueError, match="Cannot pass search config with backtrace=False."):
        _ensure_valid_search_config(invalid_config)


def test_generate_cigar_strings(reference_path: Path, target_structures: dict[str, Path]):
    with maybe_temp_directory() as working_dir:
        query_path = working_dir / "query"
        target_path = working_dir / "target"
        target_input = working_dir / "createdb_input.tsv"

        create_tsv_for_createdb(target_input, target_structures.values())
        createdb(reference_path, query_path)
        createdb(target_input, target_path)

        cigars = _generate_cigar_strings(
            query_path,
            target_path,
            DEFAULT_REFERENCE_ALIGNMENT_SEARCH_CONFIG,
            DEFAULT_REFERENCE_ALIGNMENT_CONVERTALIS_CONFIG,
            working_dir,
        )

    # The cigars frame is typical convertalis output
    assert not cigars.empty
    assert cigars.columns.tolist() == CIGAR_OUTPUT_FORMAT.split(",")

    # Reference has a fully-matching cigar string with itself
    reference_name = structure_name_and_extension(reference_path)[0] | not_none
    self_hit = cigars.query(f"target == '{reference_name}'").iloc[0]
    expected_cigar = f"{len(self_hit.qseq)}M"
    assert self_hit.cigar == expected_cigar

    # Check that one of the cigar strings matches the expected value (the 7th row was
    # chosen at random and was manually validated)
    assert cigars.iloc[7].cigar == "312M10D64M"


def test_align_to_reference(reference_path: Path, target_structures: dict[str, Path]):
    traces = align_to_reference(
        reference_structure=reference_path,
        target_structures=target_structures,
        search_config=DEFAULT_REFERENCE_ALIGNMENT_SEARCH_CONFIG,
        convertalis_config=DEFAULT_REFERENCE_ALIGNMENT_CONVERTALIS_CONFIG,
    )

    reference_name = structure_name_and_extension(reference_path)[0] | not_none
    reference_length = traces.shape[0]

    # The number of trace rows matches the reference
    assert traces.shape[0] == reference_length

    # The self-trace is an arange that equals the index
    assert (traces[reference_name].values == traces.index.values).all()  # type: ignore
    assert (traces[reference_name].values == np.arange(reference_length)).all()  # type: ignore
