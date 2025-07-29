import tempfile
from pathlib import Path

import pytest

from apb.utils import is_executable, maybe_temp_directory, require_dependency, run_command


def test_is_executable():
    # These are programs
    assert is_executable("ln")
    assert is_executable("python")

    # These are not
    assert not is_executable("not_a_program")
    assert not is_executable("definitely not a program")
    assert not is_executable("")


def test_require_dependency():
    @require_dependency("python")
    def this_runs():
        pass

    this_runs()

    @require_dependency("not_a_program")
    def this_doesnt_run():
        pass

    with pytest.raises(RuntimeError, match="not found in PATH"):
        this_doesnt_run()

    # Now test that decorator stacking behavior works.

    @require_dependency("ln")
    @require_dependency("python")
    def this_also_runs():
        pass

    this_also_runs()

    @require_dependency("python")
    @require_dependency("not_a_program")
    def this_also_doesnt_run():
        pass

    with pytest.raises(RuntimeError, match="not found in PATH"):
        this_also_doesnt_run()


def test_run_command():
    with pytest.raises(ValueError, match="Empty command"):
        run_command([])

    with pytest.raises(ValueError, match="not a program"):
        run_command(["not_a_command", "foo"])

    with pytest.raises(RuntimeError, match="name 'some_variable' is not defined"):
        run_command(["python", "-c", "print(some_variable)"])

    assert run_command(["echo", "hi"]).stdout.strip() == "hi"
    assert run_command(["python", "-c", "print(4*4)"]).stdout.strip() == "16"


def test_temp_directory_with_no_tmpdir():
    """Test the temp directory context manager without a provided temporary directory."""
    with maybe_temp_directory() as tmpdir:
        assert tmpdir.exists(), "Temporary directory should exist"
        temp_file = tmpdir / "example.txt"
        temp_file.write_text("Hello, World!")
        assert temp_file.read_text() == "Hello, World!"
    assert not tmpdir.exists(), "Temporary directory should be deleted after exiting the context"


def test_temp_directory_with_existing_tmpdir():
    """Test the temp directory context manager with a provided existing temporary directory."""
    with tempfile.TemporaryDirectory() as existing_tmpdir:
        existing_path = Path(existing_tmpdir)

        with maybe_temp_directory(existing_path) as tmpdir:
            assert tmpdir == existing_path, "Should use the existing directory"

            temp_file = tmpdir / "example.txt"
            temp_file.write_text("Temporary check")

            assert temp_file.read_text() == "Temporary check"

        assert tmpdir.exists(), "Existing temp dir should not be deleted after exiting the context"
        assert (tmpdir / "example.txt").exists(), "File should exist in the provided directory"
