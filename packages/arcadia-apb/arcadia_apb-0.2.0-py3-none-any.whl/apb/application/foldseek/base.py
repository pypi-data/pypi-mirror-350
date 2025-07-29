"""A minimalistic Foldseek wrapper

This module provides a simplified interface to some of the basic functionalities of
Foldseek. It facilitates the use of Foldseek by abstracting the command-line
interactions.

**Important Note** This is a bare-bones implementation intended for basic use cases. It
does not cover all the flags, options, or outputs available in Foldseek. The goal is to
provide a starting point that can be extended and refined as use cases develop. This is
not and will never be a feature-complete wrapper of Foldseek. Nevertheless, users
requiring advanced features or customizations can consider extending the code to meet
their use case, or make a feature request.
"""

from pathlib import Path

import pandas as pd

from apb.application.foldseek.datatypes import (
    FoldSeekConvertalisConfig,
    FoldseekOutputFileNotFoundError,
    FoldSeekSearchConfig,
)
from apb.application.foldseek.utils import format_alignment_tsv
from apb.types import Pathish
from apb.utils import maybe_temp_directory, require_dependency, run_command

FOLDSEEK_EXECUTABLE: str = "foldseek"
LOG_FOLDSEEK_OUTPUT: bool = False
DEFAULT_SEARCH_CONFIG = FoldSeekSearchConfig()
DEFAULT_CONVERTALIS_CONFIG = FoldSeekConvertalisConfig()


@require_dependency(FOLDSEEK_EXECUTABLE)
def createdb(input_path: Pathish, output_path_prefix: Pathish) -> Path:
    """Runs foldseek's createdb subcommand.

    This runs the command `foldseek createdb <input_path> <output_path_prefix>` and
    checks that the expected output path exists. No other logic is layered in. Consult
    `foldseek createdb -h` for documentation. If any flags are needed, please request
    them.

    Returns:
        Path:
            The path to the main DB file. `foldseek createdb` generates many files, all
            prefixed with this path.
    """
    input_path = Path(input_path)
    output_path_prefix = Path(output_path_prefix)

    command = [
        FOLDSEEK_EXECUTABLE,
        "createdb",
        str(input_path),
        str(output_path_prefix),
    ]
    run_command(command, log_stdout=LOG_FOLDSEEK_OUTPUT)

    if not output_path_prefix.exists():
        raise FoldseekOutputFileNotFoundError(output_path_prefix, command)

    return output_path_prefix


@require_dependency(FOLDSEEK_EXECUTABLE)
def search(
    query_path: Pathish,
    target_path: Pathish,
    alignment_path_prefix: Pathish,
    config: FoldSeekSearchConfig = DEFAULT_SEARCH_CONFIG,
) -> Path:
    """Runs foldseek's search subcommand.

    This runs the base command:

    `foldseek search <query_path> <target_path> <alignment_path_prefix> tmp`

    Additionally, some parameters can be appended to this command by specifying them
    with a `FoldSeekSearchConfig` object.

    Args:
        query_path: The input query file path.
        target_path: The input target file path.
        alignment_path_prefix: The output prefix for the alignment files.
        config:
            Configuration for the search command. If not supplied, foldseek's default
            options are used.

    Returns:
        Path: The path prefix to the alignment files.
    """
    query_path = Path(query_path)
    target_path = Path(target_path)
    alignment_path_prefix = Path(alignment_path_prefix)

    command = [
        FOLDSEEK_EXECUTABLE,
        "search",
        str(query_path),
        str(target_path),
        str(alignment_path_prefix),
        "tmp",
    ]
    command.extend(config.parameters())
    run_command(command, log_stdout=LOG_FOLDSEEK_OUTPUT)

    # The prefix doesn't itself exist, so we check for the existence of the index.
    if not alignment_path_prefix.with_suffix(".index").exists():
        raise FoldseekOutputFileNotFoundError(alignment_path_prefix, command)

    return alignment_path_prefix


@require_dependency(FOLDSEEK_EXECUTABLE)
def convertalis(
    query_path: Pathish,
    target_path: Pathish,
    alignment_path_prefix: Pathish,
    tsv_path: Pathish | None = None,
    config: FoldSeekConvertalisConfig = DEFAULT_CONVERTALIS_CONFIG,
    working_dir: Pathish | None = None,
) -> pd.DataFrame:
    """Runs foldseek's convertalis subcommand and formats the alignment TSV.

    This runs the command:

    foldseek convertalis <query_path> <target_path> <alignment_path_prefix> <tsv_path> \
        --format-mode 4 --format-output <format_output>

    `--format-mode 4` (BLAST-TAB + column headers) is hardcoded as the only possible
    output mode.

    Args:
        query_path: The input query file path.
        target_path: The input target file path.
        alignment_path_prefix: The alignment path prefix.
        tsv_path: The output TSV file path. If not provided, a temporary file will be used.
        format_output:
            An optional format string to specify which columns should be present in the
            output. For available options see `foldseek convertalis -h`.

    Returns:
        pd.DataFrame: The formatted dataframe containing alignment results.
    """
    query_path = Path(query_path)
    target_path = Path(target_path)
    alignment_path_prefix = Path(alignment_path_prefix)

    with maybe_temp_directory(working_dir) as working_dir:
        tsv_path = Path(tsv_path) if tsv_path else working_dir / "alignment.tsv"

        to_tsv_command = [
            FOLDSEEK_EXECUTABLE,
            "convertalis",
            str(query_path),
            str(target_path),
            str(alignment_path_prefix),
            str(tsv_path),
            "--format-mode",
            "4",
        ]
        to_tsv_command.extend(config.parameters())

        run_command(to_tsv_command, log_stdout=LOG_FOLDSEEK_OUTPUT)

        if not tsv_path.exists():
            raise FoldseekOutputFileNotFoundError(alignment_path_prefix, to_tsv_command)

        return format_alignment_tsv(pd.read_csv(tsv_path, sep="\t"))
