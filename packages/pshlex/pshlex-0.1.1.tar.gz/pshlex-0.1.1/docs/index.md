<!--
SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
SPDX-License-Identifier: BSD-2-Clause
-->

# pshlex - join various stringifiable objects and quote them for the shell

\[[Home][ringlet-home] | [GitLab][gitlab] | [PyPI][pypi] | [Download](download.md) | [ReadTheDocs][readthedocs]\]

## Overview

This library was written mainly to provide a function that can stringify
a list of path-like objects: the [`join()`][pshlex.join] function is very similar to
[`shlex.join()`][py-shlex-join], but it will accept [`pathlib.Path`][py-pathlib-path] objects
as well as strings.

The [`join_any()`][pshlex.join_any] function started off as an implementation detail, but
it may turn out to be useful in its own right; it is also similar to
[`shlex.join()`][py-shlex-join], but it will convert any Python object into its string
representation.

## Examples

Use the [`join()`][pshlex.join] function as a type-safe version when dealing with
path-like objects:

``` python
def run(cmd: list[str | pathlib.Path]) -> None:
"""Run a command."""
    cmdstr: Final = pshlex.join(cmd)
    ...
        sys.exit(f"Could not run `{cmdstr}`: {err}")
```

## Contact

The `pshlex` library was written by [Peter Pentchev][roam].
It is developed in [a GitLab repository][gitlab].
This documentation is hosted at [Ringlet][ringlet-home] with a copy at [ReadTheDocs][readthedocs].

[roam]: mailto:roam@ringlet.net "Peter Pentchev"
[gitlab]: https://gitlab.com/ppentchev/pshlex "The pshlex GitLab repository"
[pypi]: https://pypi.org/project/pshlex/ "The pshlex Python Package Index page"
[readthedocs]: https://pshlex.readthedocs.io/ "The pshlex ReadTheDocs page"
[ringlet-home]: https://devel.ringlet.net/textproc/pshlex/ "The Ringlet pshlex homepage"
[py-shlex-join]: https://docs.python.org/3/library/shlex.html#shlex.join "shlex.join() in the Python standard library"
[py-pathlib-path]: https://docs.python.org/3/library/pathlib.html#pathlib.Path "pathlib.Path in the Python standard library"
