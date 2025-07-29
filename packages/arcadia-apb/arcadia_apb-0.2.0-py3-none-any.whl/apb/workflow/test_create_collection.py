from pathlib import Path

import pytest
from click.testing import CliRunner
from sqlalchemy.orm.session import Session

import apb.database.collection as collection
from apb._test_pointer import TEST_RAW_COLLECTION
from apb.workflow.create_collection import (
    FeatureCalculationConfig,
    cli,
    load_feature_config,
    save_feature_config,
)


@pytest.fixture
def runner():
    return CliRunner()


def test_help(runner: CliRunner):
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Create a protein collection database" in result.output


def test_create_feature_config_file(runner: CliRunner, tmp_path: Path):
    path = tmp_path / "config.json"

    # The CLI runs and creates the config
    result = runner.invoke(cli, ["config", str(path)])
    assert result.exit_code == 0
    assert path.exists()

    # The result can be structured into a FeatureRecipe object
    load_feature_config(path)


def test_create_config_file_exists(runner: CliRunner, tmp_path: Path):
    # Create the file
    path = tmp_path / "config.json"
    path.touch()

    # Run the CLI
    result = runner.invoke(cli, ["config", str(path)])

    # It fails because the file already exists
    assert result.exit_code != 0


def test_run_with_default_config(runner: CliRunner, tmp_path: Path):
    output_db = tmp_path / "output.db"

    # The CLI runs
    result = runner.invoke(
        cli,
        [
            "run",
            "-i",
            str(TEST_RAW_COLLECTION),
            "-o",
            str(output_db),
        ],
    )
    assert result.exit_code == 0

    # The DB can be read from
    with Session(collection.get_engine(output_db)) as session:
        collection.get_profile_from_index(session, 1)


def test_run_with_custom_config(runner: CliRunner, tmp_path: Path):
    output_db = tmp_path / "output.db"
    config_path = tmp_path / "config.json"

    # Create a custom config file
    save_feature_config(FeatureCalculationConfig.default(), config_path)

    # The CLI runs
    result = runner.invoke(
        cli,
        [
            "run",
            "-i",
            str(TEST_RAW_COLLECTION),
            "-o",
            str(output_db),
            "-c",
            str(config_path),
        ],
    )
    assert result.exit_code == 0

    # The DB can be read from
    with Session(collection.get_engine(output_db)) as session:
        collection.get_profile_from_index(session, 1)
