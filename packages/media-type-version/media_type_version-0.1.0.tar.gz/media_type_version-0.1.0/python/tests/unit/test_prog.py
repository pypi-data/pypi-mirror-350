# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause
"""Make sure that `media-type-version run` starts up at least."""

from __future__ import annotations

import os
import subprocess  # noqa: S404
import sys
import typing

import pytest


if typing.TYPE_CHECKING:
    from typing import Final


PREFIX: Final = "vnd.ringlet.something/else"
"""The prefix for the media type string before the .vX.Y part."""

SUFFIX: Final = "+toml"
"""The expected suffix."""

VERSIONS: Final = [
    (42, 616),
    (0, 0),
    (0, 1),
    (3, 0),
]
"""The version combinations to test with."""


def get_prog() -> list[str]:
    """Determine the test program to run."""
    env_prog: Final = os.environ.get("TEST_MTV_EXTRACT_PROG")
    return [env_prog] if env_prog is not None else [sys.executable, "-m", "media_type_version"]


@pytest.mark.parametrize("ver_tuple", VERSIONS)
def test_run_one_by_one(*, ver_tuple: tuple[int, int]) -> None:
    """Make sure that `mtv-extract -` can parse a string."""
    prog: Final = get_prog()
    major, minor = ver_tuple
    output: Final = subprocess.check_output(  # noqa: S603
        [*prog, "-p", PREFIX, "-s", SUFFIX, "--", "-"],
        encoding="UTF-8",
        input=f"{PREFIX}.v{major}.{minor}{SUFFIX}",
    )
    assert output == f"{major}\t{minor}\n"


def test_run_all_at_once() -> None:
    """Make sure that `mtv-extract -` can parse several strings at once."""
    prog: Final = get_prog()
    output: Final = subprocess.check_output(  # noqa: S603
        [*prog, "-p", PREFIX, "-s", SUFFIX, "--", "-"],
        encoding="UTF-8",
        input="".join(f"{PREFIX}.v{major}.{minor}{SUFFIX}\n" for major, minor in VERSIONS),
    )
    assert output == "".join(f"{major}\t{minor}\n" for major, minor in VERSIONS)
