import re
from collections.abc import Iterable
from pathlib import Path

import pandas as pd
import pandera as pa

from apb.structure.utils import RECOGNIZED_STRUCTURE_FILETYPES
from apb.types import Pathish

# These are taken from `foldseek convertalis -h`. multimer measures (those prefixed with
# 'complex') are absent.
_alignment_dataframe_schema = pa.DataFrameSchema(
    {
        "query": pa.Column("str", required=False),
        "target": pa.Column("str", required=False),
        "evalue": pa.Column("float64", required=False),
        "gapopen": pa.Column("int64", required=False),
        "pident": pa.Column("float64", required=False),
        "fident": pa.Column("float64", required=False),
        "nident": pa.Column("int64", required=False),
        "qstart": pa.Column("int64", required=False),
        "qend": pa.Column("int64", required=False),
        "qlen": pa.Column("int64", required=False),
        "qaln": pa.Column("str", required=False),
        "tstart": pa.Column("int64", required=False),
        "tend": pa.Column("int64", required=False),
        "tlen": pa.Column("int64", required=False),
        "taln": pa.Column("str", required=False),
        "alnlen": pa.Column("int64", required=False),
        "bits": pa.Column("int64", required=False),
        "cigar": pa.Column("str", required=False),
        "qseq": pa.Column("str", required=False),
        "tseq": pa.Column("str", required=False),
        "qheader": pa.Column("str", required=False),
        "theader": pa.Column("str", required=False),
        "qalign": pa.Column("str", required=False),
        "talign": pa.Column("str", required=False),
        "mismatch": pa.Column("int64", required=False),
        "qcov": pa.Column("float64", required=False),
        "tcov": pa.Column("float64", required=False),
        "qset": pa.Column("str", required=False),
        "qsetid": pa.Column("int64", required=False),
        "tset": pa.Column("str", required=False),
        "tsetid": pa.Column("int64", required=False),
        "taxid": pa.Column("int64", required=False),
        "taxname": pa.Column("str", required=False),
        "taxlineage": pa.Column("str", required=False),
        "lddt": pa.Column("float64", required=False),
        "lddtfull": pa.Column("str", required=False),
        "qca": pa.Column("str", required=False),
        "tca": pa.Column("str", required=False),
        "t": pa.Column("str", required=False),
        "u": pa.Column("str", required=False),
        "qtmscore": pa.Column("float64", required=False),
        "ttmscore": pa.Column("float64", required=False),
        "alntmscore": pa.Column("float64", required=False),
        "rmsd": pa.Column("float64", required=False),
        "prob": pa.Column("float64", required=False),
    },
    coerce=True,
    strict=True,  # Enforces that all columns in the data exist in the schema
)


def format_alignment_tsv(frame: pd.DataFrame) -> pd.DataFrame:
    """Formats the alignment TSV DataFrame.

    Validates the DataFrame against a predefined schema and removes known file extensions
    from the query and target columns.

    Args:
        frame: The DataFrame containing alignment results.

    Returns:
        pd.DataFrame: The formatted dataframe.
    """
    frame = _alignment_dataframe_schema.validate(frame)

    # Foldseek only removes the first extension from file names. This is problematic
    # because if your file is `name.pdb.gz`, the name in the alignment table resolves to
    # `name.pdb` rather than `name`. We resolve this by compiling our accepted structure
    # formats into a regex.

    extension_pattern = r"|".join([re.escape(ext) for ext in RECOGNIZED_STRUCTURE_FILETYPES])

    if "query" in frame.columns:
        frame["query"] = frame["query"].str.replace(extension_pattern, "", regex=True)

    if "target" in frame.columns:
        frame["target"] = frame["target"].str.replace(extension_pattern, "", regex=True)

    return frame


def create_tsv_for_createdb(tsv_path: Pathish, structure_paths: Iterable[Pathish]) -> Path:
    """Create a TSV of structure paths that can be used as input from foldseek's `createdb`"""
    with open(tsv_path, "w") as fp:
        fp.writelines(f"{structure_path}\n" for structure_path in structure_paths)

    return Path(tsv_path)
