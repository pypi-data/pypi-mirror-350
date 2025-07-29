"""Utilities for alignment"""

import pandas as pd


def aligned_seqs_to_dataframe(seqs: list[str]) -> pd.DataFrame:
    """Convert a list of aligned (gapped) sequences to a dataframe

    Args:
        seqs: A list of strings, where each string is a gapped sequence of characters.

    Returns:
        frame:
            A DataFrame where each row corresponds to a sequence from the input list and
            each column represents a position in the sequence alignment.

    Raises:
        ValueError:
            If not all sequences in the input list are of the same length.
    """
    if not all(len(seq) == len(seqs[0]) for seq in seqs):
        raise ValueError("Not all sequences are of the same length")

    return pd.DataFrame([list(seq) for seq in seqs])
