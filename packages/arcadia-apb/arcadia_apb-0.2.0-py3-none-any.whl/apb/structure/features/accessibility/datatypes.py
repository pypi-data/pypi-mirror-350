from __future__ import annotations

import attrs

from apb.vendor.strenum import StrEnum, auto


class MaxSASASource(StrEnum):
    """Different definitions of per-residue max exposed surface area

    Attributes
        AHMAD: Ahmad et al. 2003 https://doi.org/10.1002/prot.10328
        MILLER: Miller et al. 1987 https://doi.org/10.1016/0022-2836(87)90038-6
        SANDER: Sander & Rost 1994 https://doi.org/10.1002/prot.340200303
        WILKE: Tien et al. 2013 https://doi.org/10.1371/journal.pone.0080635
    """

    AHMAD = auto()
    MILLER = auto()
    SANDER = auto()
    WILKE = auto()


@attrs.define(frozen=True)
class SolventAccessibilityConfig:
    normalize: bool
    source: MaxSASASource
    point_number: int

    @classmethod
    def default(cls) -> SolventAccessibilityConfig:
        return cls(
            normalize=True,
            source=MaxSASASource.WILKE,
            point_number=200,
        )

    @property
    def feature_name(self) -> str:
        return "relative_solvent_accessibility" if self.normalize else "solvent_accessibility"
