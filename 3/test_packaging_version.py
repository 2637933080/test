"""Pytest test cases for the open-source `packaging` library.

These tests exercise different logical branches of `packaging.version.Version`:
- Normalization of release numbers
- Pre-release comparison ordering
- Validation errors for malformed versions
"""

import pytest
from packaging.version import InvalidVersion, Version


def test_version_normalization_equates_patch_release() -> None:
    """`Version` should treat missing patch component as zero."""
    assert Version("1.0") == Version("1.0.0")


def test_pre_release_sorted_before_final_release() -> None:
    """Pre-release identifiers must sort before the final release."""
    assert Version("2.0a1") < Version("2.0")


def test_invalid_version_raises_invalid_version() -> None:
    """Malformed version strings should raise `InvalidVersion`."""
    with pytest.raises(InvalidVersion):
        Version("1..0")
