import numpy as np
import pandas as pd
from biotite.structure.residues import apply_residue_wise, get_residues
from biotite.structure.sasa import sasa

from apb.structure.features.accessibility.datatypes import MaxSASASource, SolventAccessibilityConfig
from apb.structure.features.accessibility.normalization import get_max_sasa_map
from apb.types import ProteinStructure

DEFAULT_CONFIG = SolventAccessibilityConfig.default()


def calc_solvent_accessibility(
    structure: ProteinStructure,
    config: SolventAccessibilityConfig = DEFAULT_CONFIG,
) -> pd.Series:
    atomic_sasa = sasa(structure, vdw_radii="Single", point_number=config.point_number)
    solv_acc = apply_residue_wise(structure, atomic_sasa, np.sum)

    assert solv_acc is not None

    if config.normalize:
        max_sasa_map = get_max_sasa_map(config.source)
        _, residues = get_residues(structure)

        for idx, residue in enumerate(residues):
            solv_acc[idx] /= max_sasa_map[residue]

        # Estimated RSAs can exceed slightly > 1. We enforce these residues to have RSA := 1
        solv_acc[solv_acc > 1.0] = 1.0

    return pd.Series(
        solv_acc,
        dtype="float64",
        name=config.feature_name,
    )


__all__ = [
    "SolventAccessibilityConfig",
    "MaxSASASource",
    "calc_solvent_accessibility",
]
