from __future__ import annotations

import attrs
import pandas as pd
from biotite.sequence.seqtypes import ProteinSequence

from apb.types import ProteinStructure, aa_dtype


def get_residue_index(sequence_length: int) -> pd.Index:
    return pd.Index(range(sequence_length), "uint32", name="residue_index")


@attrs.define
class ProteinProfile:
    """A protein profile dataclass

    A protein profile is data structure that integrates sequence, structure, and
    associated annotation data for an individual protein. By tying sequence and
    structure components together within a protein profile, downstream analyses that
    incorporate information from both sequence and structure (very common) is made
    easier.

    Attributes:
        name: The name of the protein.
        sequence: The amino acid sequence of the protein.
        structure: The 3D structure of the protein.
        res_features:
            A dataframe containing residue-level features, indexed by residue_index. If
            not provided, a dataframe with a single column, "amino_acid", is used.
        source:
            The metadata describing the source of the protein. Currently this is a
            placeholder empty string but could be structured into something in the
            future.
    """

    name: str
    sequence: ProteinSequence
    structure: ProteinStructure
    residue_features: pd.DataFrame = attrs.field(factory=pd.DataFrame)
    source: str = attrs.field(default="")

    def __attrs_post_init__(self) -> None:
        expected_index = get_residue_index(len(self.sequence))

        if self.residue_features.empty:
            # Empty dataframe can still have index of non-zero length
            self.residue_features.index = expected_index
        else:
            # A non-empty dataframe was passed. Ensure the shape matches
            if self.residue_features.shape[0] != len(self.sequence):
                raise ValueError(
                    f"Expected axis 0 shape to match sequence length of {len(self.sequence)}, "
                    f"but got shape {self.residue_features.shape}."
                )

        # Ensure element-by-element consistency of indices
        if not self.residue_features.index.equals(expected_index):
            raise ValueError("Dataframe indices don't match expectation (range index from 0)")

        self.residue_features.index = expected_index

        if "amino_acid" not in self.residue_features:
            self.residue_features.insert(
                0, "amino_acid", pd.Series(self.sequence.symbols, dtype=aa_dtype)
            )

    def add_feature(self, feature: pd.Series) -> None:
        """Add a new residue-level feature

        Args:
            feature:
                A pandas Series representing the new feature, with a length matching the
                protein sequence.

        Raises:
            ValueError:
                If the length of the feature does not match the sequence length, if the
                feature is unnamed, if the feature name already exists, or if the
                feature index does not match the expected index (a range from 0 ->
                sequence length).
        """
        if len(feature) != len(self.sequence):
            raise ValueError(
                f"Feature of length {len(feature)} must match sequence length {len(self.sequence)}"
            )

        if feature.name is None:
            raise ValueError("Unnamed series feature. Add a unique name")

        if feature.name in self.residue_features.columns:
            raise ValueError(f"Feature '{feature.name}' already present")

        if not feature.index.equals(self.residue_features.index):
            raise ValueError("Dataframe indices don't match expectation (range index from 0)")

        feature.index = self.residue_features.index

        self.residue_features[feature.name] = feature
