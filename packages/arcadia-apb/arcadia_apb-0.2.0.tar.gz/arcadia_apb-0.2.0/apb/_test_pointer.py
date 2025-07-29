"""Points to test files present in development

Our test files live outside the python package so they aren't inadvertently linted.

In production, none of these paths should exist. In development, all of them
should.
"""

from pathlib import Path

TEST_ROOT = Path(__file__).parent.parent / "test_data"

TEST_STRUCTURES_ROOT = TEST_ROOT / "structures"

TEST_RAW_COLLECTION = TEST_ROOT / "raw_collection"


def structure_paths() -> list[Path]:
    return sorted(list(TEST_STRUCTURES_ROOT.glob("*")))


TEST_TMALIGN_ROOT = TEST_ROOT / "tmalign"
