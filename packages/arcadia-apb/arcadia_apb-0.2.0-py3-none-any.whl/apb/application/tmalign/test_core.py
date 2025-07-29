from __future__ import annotations
from pathlib import Path

import attrs
import pytest
from biotite.sequence.seqtypes import ProteinSequence

from apb._test_pointer import TEST_STRUCTURES_ROOT, TEST_TMALIGN_ROOT
from apb.application.tmalign.core import TMAlignOutput, _parse_stdout, _run_cmd, run_tmalign


@attrs.define
class TMAlignRunBundle:
    """Houses the inputs, standard output, and structured output of a TMAlign run"""

    path1: Path
    path2: Path
    expected_standard_out: str
    expected_structured_output: TMAlignOutput

    @classmethod
    def create(
        cls, path1: Path, path2: Path, stdout_path: Path, output: TMAlignOutput
    ) -> TMAlignRunBundle:
        with open(stdout_path) as file:
            stdout = file.read()

        return TMAlignRunBundle(
            path1,
            path2,
            stdout,
            output,
        )


test_runs = [
    # Run 1
    TMAlignRunBundle.create(
        TEST_STRUCTURES_ROOT / "structure1.pdb",
        TEST_STRUCTURES_ROOT / "structure2.pdb",
        TEST_TMALIGN_ROOT / "tmalign.stdout1",
        TMAlignOutput(
            qseq_aligned="----PSIVARSNFNVCRLPGTPEALCATYTGCIIIPGATCPGDYA-",
            tseq_aligned="KSCCPTTAARNQYNICRLPGTPRPVC-------IISGTGCPP--RH",
            qtmscore=0.72678,
            ttmscore=0.79485,
            rmsd=0.58,
        ),
    ),
    # More runs can be added...
]


@pytest.fixture
def run() -> TMAlignRunBundle:
    return test_runs[0]


def test_filetype_integrity(run: TMAlignRunBundle):
    with pytest.raises(RuntimeError, match="Command failed"):
        run_tmalign(run.path1, Path("doesnt_exist.pdb"))

    with pytest.raises(RuntimeError, match="Command failed"):
        run_tmalign(Path("doesnt_exist.pdb"), run.path2)

    # Unallowed extensions fail.

    with pytest.raises(ValueError, match="TMAlign accepts the following extensions"):
        run_tmalign(run.path1.with_suffix(".cif"), run.path2)

    with pytest.raises(ValueError, match="TMAlign accepts the following extensions"):
        run_tmalign(run.path1, run.path2.with_suffix(".cif"))


@pytest.mark.parametrize("run", test_runs)
def test_run_cmd(run: TMAlignRunBundle):
    # stdout1 was generated from STRUCTURE1_PATH and STRUCTURE2_PATH, so we expect the
    # same output when we run _run_cmd.
    expected = run.expected_standard_out
    output = _run_cmd(run.path1, run.path2)

    # However, the chain names will differ, since they depend on which directory the
    # test is run within. For example e.g., "structure1.pdb" versus
    # "apb/align/tmalign/test_data/structure1.pdb". This means we cannot do a rote
    # comparison, and instead have to do a line-by-line comparison, skipping over the
    # chain name lines.
    expected_lines = expected.strip("\n").split("\n")
    output_lines = output.strip("\n").split("\n")
    for o_line, e_line in zip(output_lines, expected_lines, strict=True):
        if "Name of Chain" in o_line:
            continue
        assert o_line == e_line, f"Lines differ: {o_line} != {e_line}"


@pytest.mark.parametrize("run", test_runs)
def test_parse_stdout(run: TMAlignRunBundle):
    # Parsing the standard out should yield the structured out.
    assert _parse_stdout(run.expected_standard_out) == run.expected_structured_output


@pytest.mark.parametrize("run", test_runs)
def test_TMAlignOutput(run: TMAlignRunBundle):
    # Strip the gaps of the aligned tseq.
    expected_tseq = run.expected_structured_output.tseq_aligned.replace("-", "")

    # Ensure cached property `tseq` matches.
    assert run.expected_structured_output.tseq == expected_tseq


@pytest.mark.parametrize("run", test_runs)
def test_inverse_relationship(run: TMAlignRunBundle):
    """Test the inverse relationship

    TMalign has an inverse relationship with its inputs, whereby the alignment of query
    to target can be derived from the inverse alignment (target to query). While this is
    conceptually true, and in practice it is almost always true, sometimes TMAlign has
    different outputs. However, these differences are rare and slight.
    """
    out1 = run_tmalign(run.path1, run.path2)
    out2 = run_tmalign(run.path2, run.path1)

    assert out1.qseq_aligned == out2.tseq_aligned
    assert out1.tseq_aligned == out2.qseq_aligned
    assert out1.qtmscore == out2.ttmscore
    assert out1.ttmscore == out2.qtmscore


@pytest.mark.parametrize("run", test_runs)
def test_to_biotite(run: TMAlignRunBundle):
    out = run_tmalign(run.path1, run.path2)
    alignment = out.to_biotite()

    assert alignment.sequences[0] == ProteinSequence(out.qseq)
    assert alignment.sequences[1] == ProteinSequence(out.tseq)

    # The entirety of both sequences are found in the trace. Test this by observing the
    # ends of each sequence (0 and len(seq)-1).
    assert 0 in alignment.trace[:, 0]
    assert 0 in alignment.trace[:, 1]
    assert len(out.qseq) - 1 in alignment.trace[:, 0]
    assert len(out.tseq) - 1 in alignment.trace[:, 1]
