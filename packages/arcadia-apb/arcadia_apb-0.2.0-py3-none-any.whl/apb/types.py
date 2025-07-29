from collections.abc import Mapping
from pathlib import Path
from typing import Protocol, TypeVar, overload

import pandas as pd
from biotite.structure.atoms import AtomArray, AtomArrayStack

ProteinStructure = AtomArray | AtomArrayStack

Pathish = str | Path


class StructuralReferenceAligner(Protocol):
    """A structural aligner protocol.

    This class defines a call signature that functions that align proteins to a
    reference are expected to comply with. There is intentionally no implementation.
    """

    def __call__(
        self, reference_structure: Pathish, target_structures: Mapping[str, Pathish]
    ) -> pd.DataFrame:
        """Per-residue alignment of proteins to a reference based on structural similarity.

        Returns an alignment trace that mimics the datastructure used in biotite:

            "The trace is a (m x n) ndarray with alignment length m and sequence count n.
            Each element of the trace is the index in the corresponding sequence. A gap is
            represented by the value -1."
                - (https://www.biotite-python.org/apidoc/biotite.sequence.align.Alignment.html)

        For example, the following alignment:

        CGTCAT--
        --TCATGC

        Has the following alignment trace:

        [[ 0 -1]
         [ 1 -1]
         [ 2  0]
         [ 3  1]
         [ 4  2]
         [ 5  3]
         [-1  4]
         [-1  5]]

        Args:
            reference_structure: Path to the reference structure file.
            target_structures: Dictionary with keys as names and values as structure paths.

        Returns:
            pd.DataFrame:
                A dataframe of the alignment trace. Each column is a target hit to the
                reference. The indices are the reference residue indices.
        """
        ...


_amino_acids: list[str] = [
    "A",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "K",
    "L",
    "M",
    "N",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "V",
    "W",
    "Y",
]

_amino_acids_gapped = _amino_acids + ["-"]

# The 20 canonical amino acids
aa_dtype = pd.CategoricalDtype(categories=_amino_acids)

# The 20 canonical amino acids and the gap character
aa_gapped_dtype = pd.CategoricalDtype(categories=_amino_acids_gapped)

# Secondary structure (3-state): [a]lpha helix, [b]eta sheet, [c]oil
ss3_dtype = pd.CategoricalDtype(categories=["a", "b", "c"])


T = TypeVar("T")


class NotNone:
    """A utility class ensure values are not None in a type-safe manner.

    This class allows for a convenient way to ensure that a value is not None using the
    | operator or __call__. If the value is None, a ValueError is raised. This lets type
    checkers to infer that the value is not None after the operation.

    Examples:

        All three of these examples either prevent or ignore a type checking error, but
        the last method is preferred.

        1. Sloppy

        >>> ans = func_returns_str_or_none()
        >>> ans.split(" ")  # type: ignore

        - Error is ignored
        - The type of `ans` is ignored altogether

        2. Better

        >>> ans = func_returns_str_or_none()
        >>> assert ans is not None
        >>> ans.split(" ")

        - Explicit
        - `ans` is type-checked as a string
        - If run with python -O, this is not runtime safe
        - Verbose

        3. Best

        >>> ans = func_returns_str_or_none() | not_none
        >>> ans.split(" ")

        OR

        >>> ans = not_none(func_returns_str_or_none())
        >>> ans.split(" ")

        - Explicit
        - Runtime safe
        - Understood by type checkers
    """

    @overload
    def __ror__(self, other: T | None) -> T: ...

    @overload
    def __ror__(self, other: T) -> T: ...

    def __ror__(self, other: T | None) -> T:
        return self._not_none(other)

    def __call__(self, value: T | None) -> T:
        return self._not_none(value)

    def _not_none(self, obj: T | None) -> T:
        if obj is None:
            raise ValueError("Value cannot be None")
        return obj


not_none = NotNone()
