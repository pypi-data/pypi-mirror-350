# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause
"""Join various stringifiable objects and quote them for the shell.

This library was written mainly to provide a function that can stringify
a list of path-like objects: the `join()` function is very similar to
`shlex.join`, but it will accept `pathlib.Path` objects as well as strings.

The `join_any()` function started off as an implementation detail, but
it may turn out to be useful in its own right; it is also similar to
`shlex.join()`, but it will convert any Python object into its string
representation.
"""

from __future__ import annotations

import shlex
import typing


if typing.TYPE_CHECKING:
    import pathlib
    from collections.abc import Iterable
    from typing import Any, Final


VERSION: Final = "0.1.1"
"""The pshlex library version, semver-like."""


FEATURES: Final = {
    "pshlex": VERSION,
    "join": "1.0",
    "join_any": "1.0",
}
"""The list of features supported by the pshlex library."""


def join(values: Iterable[str | pathlib.Path]) -> str:
    """Join a list of path-like objects and quote the result for the shell."""
    return join_any(values)


def join_any(values: Iterable[Any]) -> str:
    """Join a list of any stringifiable objects and quote the result for the shell."""
    return shlex.join(str(word) for word in values)
