# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause
"""Basic test for file importing."""

from __future__ import annotations

import re
import typing

from packaging import version as pkg_version

import pshlex


_RE_FEATURE_VALUE: Final = re.compile(
    r"^ (?P<major> 0 | [1-9][0-9]* ) \. (?P<minor> 0 | [1-9][0-9]* )",
    re.X,
)


if typing.TYPE_CHECKING:
    from typing import Final


def test_version() -> None:
    """Make sure the `VERSION` variable has a sane value."""
    version: Final = pkg_version.Version(pshlex.VERSION)
    assert version > pkg_version.Version("0")


def test_features() -> None:
    """Make sure that the list of features looks right.

    It must include the program's name, and each value must be a X.Y number pair.
    """
    assert pshlex.FEATURES["pshlex"] == pshlex.VERSION
    for value in (value for name, value in pshlex.FEATURES.items() if name != "pshlex"):
        assert _RE_FEATURE_VALUE.match(value)
