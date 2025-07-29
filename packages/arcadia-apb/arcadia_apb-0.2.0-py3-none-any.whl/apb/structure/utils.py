import logging
from collections.abc import Generator
from pathlib import Path

import attrs
import numpy as np

from apb.types import Pathish, ProteinStructure

EQUIVALENCY_TOLERANCE: float = 1e-5

RECOGNIZED_STRUCTURE_FILETYPES: set[str] = {".pdb", ".pdbx", ".pdb.gz", ".bcif", ".cif"}


def structure_name_and_extension(path: Pathish) -> tuple[str | None, str | None]:
    """Extract the base name and supported structure file extension of a path if it exists

    This only finds structure file extensions if they are supported for parsing. It
    includes commonly used compound extensions (.pdb.gz). For a list of supported
    extensions, see EXTENSION_SCOPE.

    Args:
        path: The file path from which to extract the base name and structure extension.

    Returns:
        tuple[str | None, str | None]:
            A tuple containing the base name and the extension if it is supported.
            If unsupported or unrecognized, returns (None, None).

    Examples:
        - For a path 'example.pdb', it returns ('example', '.pdb').
        - For a path 'example.pdb.gz', it returns ('example', '.pdb.gz').
        - For a path 'example', it returns (None, None).
    """
    path = Path(path)
    suffixes = path.suffixes

    combined_suffix = ""
    for suffix in reversed(suffixes):
        combined_suffix = suffix + combined_suffix
        if combined_suffix in RECOGNIZED_STRUCTURE_FILETYPES:
            base_name = path.name[: -len(combined_suffix)]
            return base_name, combined_suffix

    return None, None


def extension_matches(path: Pathish, match_set: set[str] = RECOGNIZED_STRUCTURE_FILETYPES) -> bool:
    """Returns whether the path has an extension matching the set of specified file extensions."""
    if not match_set.issubset(RECOGNIZED_STRUCTURE_FILETYPES):
        raise ValueError(f"Members of `match_set` must belong to {RECOGNIZED_STRUCTURE_FILETYPES}.")

    return structure_name_and_extension(path)[1] in match_set


@attrs.define
class _StructureFileSearchSummary:
    """Logging accumulator for `find_structure_paths`"""

    num_hits: int = attrs.field(default=0)
    num_misses: int = attrs.field(default=0)
    hit_exts: set[str] = attrs.field(factory=set)
    miss_exts: set[str] = attrs.field(factory=set)

    def add_hit(self, ext: str) -> None:
        self.num_hits += 1
        self.hit_exts.add(ext)

    def add_miss(self, ext: str) -> None:
        self.num_misses += 1
        self.miss_exts.add(ext)

    def summary(self) -> str:
        return (
            f"Number of structure files parsed: {self.num_hits}; "
            f"Number of non-structure files skipped: {self.num_misses}; "
            f"Unique structure file extensions: {self.hit_exts}; "
            f"Unique non-structure file extensions: {self.miss_exts}"
        )


def find_structure_paths(dir: Pathish) -> Generator[Path, None, _StructureFileSearchSummary]:
    summary = _StructureFileSearchSummary()

    dir = Path(dir)

    if not dir.is_dir():
        raise ValueError(f"{dir} is not a dir.")

    for path in dir.rglob("*"):
        if path.is_dir():
            continue

        _, valid_ext = structure_name_and_extension(path)

        if valid_ext is None:
            summary.add_miss("" if not len(path.suffix) else path.suffix)
            continue

        summary.add_hit(valid_ext)
        yield path

    logging.info(summary.summary())
    return summary


def structures_almost_equal(
    structure1: ProteinStructure,
    structure2: ProteinStructure,
    rtol: float = EQUIVALENCY_TOLERANCE,
) -> bool:
    """Compare two structures with tolerance for floating-point imprecision.

    Biotite implements a strict __eq__ method with no float precision leniency, so the
    `==` operator can yield False merely due to imprecisions introduced by isomorphic
    transformations and I/O operations.

    This function implements a looser comparison, allowing for a relative tolerance of
    array elements of `rtol`.

    Parameters:
        structure1: The first protein structure to compare.
        structure2: The second protein structure to compare.

    Returns:
        bool: True if the structures are considered equivalent, otherwise False.

    Notes:
        - For precise comparison, use `structure1 == structure2`
        - Implementation is borrowed from the essence of biotite structure __eq__ logic
          (from biotite/structure/atoms.py) and lower the standard by replacing
          array_equal calls with allclose calls.
    """

    # Biotite implements a strict __eq__ method
    if structure1 == structure2:
        return True

    # Check coordinates equivalence
    if structure1._coord is None or structure2._coord is None:
        return False
    if not np.allclose(structure1._coord, structure2._coord, rtol=rtol):
        return False

    if sorted(structure1._annot.keys()) != sorted(structure2._annot.keys()):
        return False

    # Check annotation values equivalence
    for name in structure1._annot:
        float_castable = True
        try:
            structure1._annot[name].astype(float)
            structure2._annot[name].astype(float)
        except ValueError:
            float_castable = False

        if float_castable:
            # Compare float-casted arrays
            if not np.allclose(
                structure1._annot[name].astype(float),
                structure2._annot[name].astype(float),
                rtol=rtol,
            ):
                return False
        else:
            if not np.array_equal(structure1._annot[name], structure2._annot[name]):
                return False

    if structure1._bonds != structure2._bonds:
        return False

    # Check box equivalence
    if structure1._box is None and structure2._box is None:
        pass  # Both are None, so equivalent in this context
    elif structure1._box is not None and structure2._box is not None:
        if not np.allclose(structure1._box, structure2._box, rtol=rtol):
            return False
    else:
        return False

    return True
