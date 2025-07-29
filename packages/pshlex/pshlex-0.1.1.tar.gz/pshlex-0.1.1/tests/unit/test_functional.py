# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause
"""Make sure that `pshlex run` starts up at least."""

from __future__ import annotations

import pathlib

import pshlex


def test_join() -> None:
    """Test the `pshlex.join()` function."""
    assert (
        pshlex.join(["ls", "-l", "--", "something' weird", pathlib.Path("/mount/weird things")])
        == "ls -l -- 'something'\"'\"' weird' '/mount/weird things'"
    )


def test_join_any() -> None:
    """Test the `pshlex.join_any()` function."""
    assert pshlex.join_any(["touch", "hello there", 5, None]) == "touch 'hello there' 5 None"
