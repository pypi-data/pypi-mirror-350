from pathlib import Path

import attrs
import pandas as pd
import pytest

from apb._test_pointer import TEST_RAW_COLLECTION
from apb.application.foldseek.base import (
    DEFAULT_CONVERTALIS_CONFIG,
    DEFAULT_SEARCH_CONFIG,
    convertalis,
    createdb,
    format_alignment_tsv,
    search,
)
from apb.application.foldseek.datatypes import FoldSeekConvertalisConfig, FoldSeekSearchConfig
from apb.utils import maybe_temp_directory


def test_createdb(tmp_path: Path):
    input_path = TEST_RAW_COLLECTION
    output_path_prefix = tmp_path / "output_db"

    # Sensible error message when path doesn't exist.
    with pytest.raises(RuntimeError, match="does not exist"):
        createdb(Path("nonexistant_path"), output_path_prefix)

    # Sensible error message when output requested is a directory.
    (tmp_path / "directory").mkdir()
    with pytest.raises(RuntimeError, match="Can not open"):
        createdb(input_path, (tmp_path / "directory"))

    # This runs without error and all expected DB files exist.
    createdb(input_path, output_path_prefix)
    assert output_path_prefix.exists()
    assert output_path_prefix.with_suffix(".dbtype").exists()
    assert output_path_prefix.with_suffix(".index").exists()
    assert output_path_prefix.with_suffix(".lookup").exists()
    assert output_path_prefix.with_suffix(".source").exists()

    output_ss = output_path_prefix.parent / (output_path_prefix.name + "_ss")
    assert output_ss.exists()
    assert output_ss.with_suffix(".dbtype").exists()
    assert output_ss.with_suffix(".index").exists()

    output_ca = output_path_prefix.parent / (output_path_prefix.name + "_ca")
    assert output_ca.exists()
    assert output_ca.with_suffix(".dbtype").exists()
    assert output_ca.with_suffix(".index").exists()

    output_h = output_path_prefix.parent / (output_path_prefix.name + "_h")
    assert output_h.exists()
    assert output_h.with_suffix(".dbtype").exists()
    assert output_h.with_suffix(".index").exists()


def test_search_config_parameters():
    default_config = FoldSeekSearchConfig()

    # Default parmeters are empty.
    assert default_config.parameters() == []

    # Each parameter modifies the parameters accordingly.

    config = attrs.evolve(default_config, backtrace=True)
    assert config.parameters() == ["-a"]

    config = attrs.evolve(default_config, backtrace=False)
    assert config.parameters() == []

    config = attrs.evolve(default_config, alignment_type=0)
    assert config.parameters() == ["--alignment-type", "0"]

    config = attrs.evolve(default_config, prefilter_mode=1)
    assert config.parameters() == ["--prefilter-mode", "1"]

    config = attrs.evolve(default_config, exact_tmscore=1)
    assert config.parameters() == ["--exact-tmscore", "1"]

    config = attrs.evolve(default_config, tmalign_fast=0)
    assert config.parameters() == ["--tmalign-fast", "0"]


def test_convertalis_config_parameters():
    default_config = FoldSeekConvertalisConfig()

    # Default parmeters are empty.
    assert default_config.parameters() == []

    # Each parameter modifies the parameters accordingly.

    config = attrs.evolve(default_config, exact_tmscore=1)
    assert config.parameters() == ["--exact-tmscore", "1"]

    config = attrs.evolve(default_config, format_output="query,qlen,target,tlen")
    assert config.parameters() == ["--format-output", "query,qlen,target,tlen"]


def test_search(tmp_path: Path):
    query_path = tmp_path / "query_db"
    target_path = tmp_path / "target_db"
    alignment_path_prefix = tmp_path / "ali"
    config = FoldSeekSearchConfig()

    # The DB paths must exist.
    with pytest.raises(RuntimeError, match="does not exist"):
        search(query_path, target_path, alignment_path_prefix, config)

    createdb(TEST_RAW_COLLECTION, query_path)
    createdb(TEST_RAW_COLLECTION, target_path)

    # This runs without error and all expected DB files exist.
    search(query_path, target_path, alignment_path_prefix, config)
    assert alignment_path_prefix.with_suffix(".dbtype").exists()
    assert alignment_path_prefix.with_suffix(".index").exists()


@pytest.fixture
def convertalis_missing_db_paths(tmp_path: Path) -> tuple[Path, Path, Path]:
    """Fixture of the non-existant paths required for convertalis"""
    query_path = tmp_path / "query_db"
    target_path = tmp_path / "target_db"
    alignment_path_prefix = tmp_path / "ali"
    return query_path, target_path, alignment_path_prefix


@pytest.fixture
def convertalis_db_paths(
    convertalis_missing_db_paths: tuple[Path, Path, Path],
) -> tuple[Path, Path, Path]:
    """Fixture of the existant paths required for convertalis"""
    query_path, target_path, alignment_path_prefix = convertalis_missing_db_paths

    # Create the query, target, and alignment DBs
    createdb(TEST_RAW_COLLECTION, query_path)
    createdb(TEST_RAW_COLLECTION, target_path)
    search(query_path, target_path, alignment_path_prefix)

    return query_path, target_path, alignment_path_prefix


def test_convertalis_db_paths_dont_exist(convertalis_missing_db_paths: tuple[Path, Path, Path]):
    query_path, target_path, alignment_path_prefix = convertalis_missing_db_paths

    # The query and target DBs must exist
    with pytest.raises(RuntimeError, match="does not exist"):
        convertalis(query_path, target_path, alignment_path_prefix)

    # Both DBs must exist
    createdb(TEST_RAW_COLLECTION, query_path)
    with pytest.raises(RuntimeError, match="does not exist"):
        convertalis(query_path, target_path, alignment_path_prefix)


def test_convertalis_alignment_doesnt_exist(convertalis_missing_db_paths: tuple[Path, Path, Path]):
    query_path, target_path, alignment_path_prefix = convertalis_missing_db_paths

    # Create the query and target DBs
    createdb(TEST_RAW_COLLECTION, query_path)
    createdb(TEST_RAW_COLLECTION, target_path)

    # The alignment must exist.
    with pytest.raises(RuntimeError, match="does not exist"):
        convertalis(query_path, target_path, alignment_path_prefix)


def test_convertalis_runs_successfully(convertalis_db_paths: tuple[Path, Path, Path]):
    query_path, target_path, alignment_path_prefix = convertalis_db_paths

    with maybe_temp_directory() as tmpdir:
        tsv_output = tmpdir / "out.tsv"

        # With all files in place, convertalis runs successfully.
        result_df = convertalis(query_path, target_path, alignment_path_prefix, tsv_output)

        # Verify that the expected TSV file exists
        assert tsv_output.exists()

        # The raw TSV has the same column headers as the output result.
        tsv_as_frame = pd.read_csv(tsv_output, sep="\t")
        assert tsv_as_frame.columns.equals(result_df.columns)

        # But they aren't equal until the TSV is validated by pandera.
        assert not tsv_as_frame.equals(result_df)
        assert format_alignment_tsv(tsv_as_frame).equals(result_df)


def test_convertalis_custom_format(convertalis_db_paths: tuple[Path, Path, Path]):
    query_path, target_path, alignment_path_prefix = convertalis_db_paths
    config = FoldSeekSearchConfig()

    # Create the query, target, and alignment DBs
    createdb(TEST_RAW_COLLECTION, query_path)
    createdb(TEST_RAW_COLLECTION, target_path)
    search(query_path, target_path, alignment_path_prefix, config)

    # Custom formats are possible.
    custom_config = attrs.evolve(DEFAULT_CONVERTALIS_CONFIG, format_output="query,qlen,qseq,pident")
    custom_result = convertalis(
        query_path,
        target_path,
        alignment_path_prefix,
        config=custom_config,
    )
    assert custom_config.format_output is not None
    assert custom_result.columns.tolist() == custom_config.format_output.split(",")


def test_convertalis_unrecognized_format(convertalis_db_paths: tuple[Path, Path, Path]):
    query_path, target_path, alignment_path_prefix = convertalis_db_paths
    config = FoldSeekSearchConfig()

    # Create the query, target, and alignment DBs
    createdb(TEST_RAW_COLLECTION, query_path)
    createdb(TEST_RAW_COLLECTION, target_path)
    search(query_path, target_path, alignment_path_prefix, config)

    # Unrecognized metrics are caught.
    custom_config = attrs.evolve(DEFAULT_CONVERTALIS_CONFIG, format_output="query,target,foo")
    with pytest.raises(RuntimeError, match="Format code foo does not exist"):
        convertalis(
            query_path,
            target_path,
            alignment_path_prefix,
            config=custom_config,
        )


def test_convertalis_with_backtrace(convertalis_db_paths: tuple[Path, Path, Path]):
    query_path, target_path, alignment_path_prefix = convertalis_db_paths
    config = FoldSeekSearchConfig()

    # Create the query, target, and alignment DBs
    createdb(TEST_RAW_COLLECTION, query_path)
    createdb(TEST_RAW_COLLECTION, target_path)
    search(query_path, target_path, alignment_path_prefix, config)

    # Some metrics require `search` to have been run with backtrace!
    custom_config = attrs.evolve(DEFAULT_CONVERTALIS_CONFIG, format_output="query,target,qaln,taln")
    with pytest.raises(RuntimeError, match="Please recompute the alignment with the -a flag"):
        convertalis(
            query_path,
            target_path,
            alignment_path_prefix,
            config=custom_config,
        )

    # After recomputing the search with the backtrace, it works.
    search(
        query_path,
        target_path,
        alignment_path_prefix,
        attrs.evolve(DEFAULT_SEARCH_CONFIG, backtrace=True),
    )
    custom_result = convertalis(
        query_path,
        target_path,
        alignment_path_prefix,
        config=custom_config,
    )
    assert custom_config.format_output is not None
    assert custom_result.columns.tolist() == custom_config.format_output.split(",")
