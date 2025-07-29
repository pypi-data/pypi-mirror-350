import pandas as pd
import pytest

from apb.sequence.utils import aligned_seqs_to_dataframe


@pytest.fixture
def alignments() -> list[str]:
    return [
        "ATGC---ATGC",
        "ATGC---ATGC",
        "ATGCAAAATGC",
        "ATGCGGGATGC",
    ]


def test_aligned_seqs_to_frame(alignments):
    expected = pd.DataFrame(
        {
            0: ["A", "A", "A", "A"],
            1: ["T", "T", "T", "T"],
            2: ["G", "G", "G", "G"],
            3: ["C", "C", "C", "C"],
            4: ["-", "-", "A", "G"],
            5: ["-", "-", "A", "G"],
            6: ["-", "-", "A", "G"],
            7: ["A", "A", "A", "A"],
            8: ["T", "T", "T", "T"],
            9: ["G", "G", "G", "G"],
            10: ["C", "C", "C", "C"],
        }
    )

    # aligned_seqs_to_frame should produce expected
    assert aligned_seqs_to_dataframe(alignments).equals(expected)

    # Raises error if additional sequence has mismatched length
    with pytest.raises(ValueError, match="Not all sequences are of the same length"):
        # Add sequence that is too long
        alignments.append("ATGCGGGATGCATGCGGGATGCATGCGGGATGC")
        aligned_seqs_to_dataframe(alignments)
