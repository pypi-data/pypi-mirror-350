from functools import cached_property
from pathlib import Path

import attrs
from biotite.sequence.align.alignment import Alignment
from biotite.sequence.seqtypes import ProteinSequence

from apb.structure.utils import extension_matches
from apb.types import Pathish
from apb.utils import require_dependency, run_command

TMALIGN_EXECUTABLE: str = "TMalign"
ALLOWED_TMALIGN_EXTENSIONS: set[str] = {".pdb"}


@attrs.define
class TMAlignOutput:
    """A dataclass representing TMAlign output.

    Attributes:
        qseq_aligned: The aligned (with gap characters) sequence of the query (protein 1).
        tseq_aligned: The aligned (with gap characters) sequence of the target (protein 2).
        qtmscore: TM-score normalized by length of the query (protein 1).
        ttmscore: TM-score normalized by length of the target (protein 2).
        rmsd: Root mean squared distance (RSMD) in angstroms between query and target.

    Properties:
        qseq: The unaligned, gapless sequence of the query (protein 1).
        tseq: The unaligned, gapless sequence of the target (protein 2).
        aligned:
            TMalign outputs the alignment characters in the stdout that specify distance
            categories between aligned residue pairs. ":" and "." denote aligned residue
            pairs <5.0 and >5.0 Angstroms, respectively, while " " denotes unaligned
            residues. This bespoke format is simplified in this property, which simply
            denotes alignment or not.
    """

    qseq_aligned: str
    tseq_aligned: str
    qtmscore: float
    ttmscore: float
    rmsd: float

    def __attrs_post_init__(self):
        assert len(self.qseq_aligned) == len(self.tseq_aligned) == len(self.aligned)

    @cached_property
    def aligned(self) -> list[bool]:
        """Returns whether alignment indices correspond to a matched state.

        Returns:
            A list of booleans as long as the alignment length. True means the alignment
            position corresponds to two matched residues, whereas False means at least
            one position is a gap. Two residues are matched if they are within 5
            Angstroms of each other.
        """
        return [
            q != "-" and t != "-" for q, t in zip(self.qseq_aligned, self.tseq_aligned, strict=True)
        ]

    @cached_property
    def alntmscore(self) -> float:
        """Calculate TM-score as aligned by the aligned length.

        The aligned length is measured from the first aligned residue pair to the last
        aligned residue pair. The `alntmscore` is a quantity popularized in Foldseek,
        and is useful to have for TMalign for a more apples-to-apples comparison.
        """
        raw_tmscore1 = self.qtmscore * len(self.qseq)
        raw_tmscore2 = self.ttmscore * len(self.tseq)
        raw_tmscore = (raw_tmscore1 + raw_tmscore2) / 2

        return raw_tmscore / self.alnlen

    @cached_property
    def alnlen(self) -> int:
        align_start = self.aligned.index(True)
        align_stop = len(self.aligned) - self.aligned[::-1].index(True)
        return align_stop - align_start

    @cached_property
    def qseq(self) -> str:
        """Returns the sequence of the unaligned (no gapped characters) query."""
        return self.qseq_aligned.replace("-", "")

    @cached_property
    def tseq(self) -> str:
        """Returns the sequence of the unaligned (no gapped characters) target."""
        return self.tseq_aligned.replace("-", "")

    def to_biotite(self) -> Alignment:
        return Alignment(
            sequences=[ProteinSequence(self.qseq), ProteinSequence(self.tseq)],
            trace=Alignment.trace_from_strings([self.qseq_aligned, self.tseq_aligned]),
        )


def _run_cmd(query: Path, target: Path) -> str:
    """Runs TMalign for two structure files.

    Args:
        query: Path to the first PDB file.
        target: Path to the second PDB file.

    Raises:
        subprocess.CalledProcessError: Anything caught by subprocess.

    Returns:
        stdout: The stdout as a string.
    """
    cmd = [
        TMALIGN_EXECUTABLE,
        str(query),
        str(target),
    ]

    return run_command(cmd).stdout


def _parse_stdout(stdout: str) -> TMAlignOutput:
    """Structures the data in the stdout of the TMAlign program.

    Args:
        stdout:
            The stdout of the TMAlign expressed as a string. For an example, see
            ./test_data/tmalign.stdout1

    Returns:
        output: A structured output of the stdout provided by TMAlign.
    """
    lines = stdout.strip("\n").split("\n")

    if (num_lines := len(lines)) != 24:
        raise ValueError(
            f"Unexpected number of lines in stdout, expected 24 lines, got {num_lines}"
        )

    qseq_aligned = lines[21]
    tseq_aligned = lines[23]

    qtmscore = float(lines[16].split("=")[1].split()[0])
    ttmscore = float(lines[17].split("=")[1].split()[0])

    rmsd_line = lines[15]
    if "RMSD" not in rmsd_line:
        raise ValueError("Parsed wrong line for RMSD.")

    rmsd = float(rmsd_line.split(",")[1].split("=")[1].split(",")[0])

    return TMAlignOutput(
        qseq_aligned=qseq_aligned,
        tseq_aligned=tseq_aligned,
        qtmscore=qtmscore,
        ttmscore=ttmscore,
        rmsd=rmsd,
    )


@require_dependency(TMALIGN_EXECUTABLE)
def run_tmalign(query: Pathish, target: Pathish) -> TMAlignOutput:
    """Facilitates the running of TMAlign and the structuring of its output.

    Args:
        query: Path to the first protein data file.
        target: Path to the second protein data file.

    Returns:
        output: An object representing the structured data of the TMalign output.
    """
    query = Path(query)
    target = Path(target)

    _msg = (
        f"TMAlign accepts the following extensions: {ALLOWED_TMALIGN_EXTENSIONS}. The following "
        f"file has an invalid extension:"
    )

    if not extension_matches(query, ALLOWED_TMALIGN_EXTENSIONS):
        raise ValueError(f"{_msg} {query}")

    if not extension_matches(target, ALLOWED_TMALIGN_EXTENSIONS):
        raise ValueError(f"{_msg} {target}")

    return _parse_stdout(_run_cmd(Path(query), Path(target)))
