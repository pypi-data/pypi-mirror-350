<!--
SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
SPDX-License-Identifier: BSD-2-Clause
-->

# Changelog

All notable changes to the pshlex project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.1] - 2025-05-24

### Other changes

- Documentation deployment:
    - switch from `tool.publync.format.version` to `tool.publync.mediaType`
- Test suite:
    - use the `uvoxen` tool to configure and run the various tests
    - bump some dependency versions so that `uv --resolution=lowest` works
    - use `ruff` 0.11.11 with no changes
    - drop the `pytest` 7.x test environment, only test with 8.x

## [0.1.0] - 2025-01-26

### Started

- First public release.

[Unreleased]: https://gitlab.com/ppentchev/pshlex/-/compare/release%2F0.1.1...main
[0.1.1]: https://gitlab.com/ppentchev/pshlex/-/tags/release%2F0.1.1
[0.1.0]: https://gitlab.com/ppentchev/pshlex/-/tags/release%2F0.1.0
