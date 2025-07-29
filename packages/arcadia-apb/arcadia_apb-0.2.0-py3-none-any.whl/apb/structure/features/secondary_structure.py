import pandas as pd
from biotite.structure.sse import annotate_sse

from apb.types import ProteinStructure, ss3_dtype

FEATURE_NAME = "secondary_structure"


def calc_3_state_secondary_structure(structure: ProteinStructure) -> pd.Series:
    sse_array = annotate_sse(structure)
    return pd.Series(sse_array, dtype=ss3_dtype, name=FEATURE_NAME)


__all__ = [
    "calc_3_state_secondary_structure",
]
