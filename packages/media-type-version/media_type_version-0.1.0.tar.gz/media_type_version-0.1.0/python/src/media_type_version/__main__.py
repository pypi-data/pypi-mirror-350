# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause
"""Do things, or do other things."""

from __future__ import annotations

import dataclasses
import pathlib
import sys
import typing
from typing import Annotated

import cappa

from . import defs
from . import impl
from . import util


if typing.TYPE_CHECKING:
    from typing import Final


@dataclasses.dataclass(frozen=True)
class MtvExtract:
    """Extract the format version from a media type string."""

    prefix: Annotated[str, cappa.Arg(short=True, long=True)]
    """The prefix to expect in the media type string."""

    quiet: Annotated[bool, cappa.Arg(short=True, long=True)]
    """Quiet operation; only display warnings and error messages."""

    verbose: Annotated[bool, cappa.Arg(short=True, long=True)]
    """Verbose operation; display diagnostic messages."""

    files: list[str]
    """The files to parse; `-` denotes the standard input stream."""

    suffix: Annotated[str, cappa.Arg(short=True, long=True)] = ""
    """The optional suffix in the media type string."""


def do_parse_file(cfg: defs.Config, fname: str, contents: str) -> None:
    """Read media type strings from a file, parse them."""
    for line in contents.splitlines():
        try:
            ver_major, ver_minor = impl.extract(cfg, line)
        except defs.MTVError as err:
            sys.exit(f"Could not parse a {fname} line: {line!r}: {err}")

        print(f"{ver_major}\t{ver_minor}")


def parse_file(cfg: defs.Config, fname: str) -> None:
    """Parse a single file containing media type strings."""
    if fname == "-":
        cfg.log.info("Reading from the standard input stream")
        contents = sys.stdin.read()
        fname = "(standard input)"
    else:
        cfg.log.info("Reading the contents of %(fname)s", {"fname": fname})
        try:
            contents = pathlib.Path(fname).read_text(encoding="UTF-8")
        except OSError as err:
            sys.exit(f"Could not read {fname}: {err}")

    cfg.log.debug("Read %(count)d characters", {"count": len(contents)})
    do_parse_file(cfg, fname, contents)


def main() -> None:
    """Parse command-line options, read files, extract data."""
    args: Final = cappa.parse(MtvExtract, completion=False)
    cfg: Final = defs.Config(
        log=util.build_logger(quiet=args.quiet, verbose=args.verbose),
        prefix=args.prefix,
        suffix=args.suffix,
    )
    for fname in args.files:
        parse_file(cfg, fname)


if __name__ == "__main__":
    main()
