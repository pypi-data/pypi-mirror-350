<!--
SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
SPDX-License-Identifier: BSD-2-Clause
-->

# media-type-version - extract the format version from a media type string

\[[Home][ringlet-home] | [GitLab][gitlab] | [PyPI][pypi] | [Python API][ringlet-api-python] | [ReadTheDocs][readthedocs]\]

## Overview

The `media-type-version` library is designed to be used as the first step in
parsing structured data, e.g. configuration files, serialized classes, etc.
The caller extracts the media type string (e.g. a JSON `"mediaType": "..."` key) and
passes it in for parsing.
The caller then decides what to do with the extracted version information -
is this version supported, what fields are expected to be there, should any
extraneous fields produce errors, and so on.

The media type string is expected to be in a `<prefix>.vX.Y<suffix>` format, with
a fixed prefix and suffix.
The prefix will usually be a vendor-specific media type.
The version part consists of two unsigned integer numbers.
The suffix, if used, may correspond to the file format.
A sample media type string identifying a TOML configuration file for
a text-processing program could be
`vnd.ringlet.textproc.publync.config/publync.v0.2+toml`

## The library

The `media-type-version` library provides a single function, `extract()`, that
parses a media type string, strips the specified prefix and suffix, and looks for
a `.vX.Y` version string left.
It then returns the (`X`, `Y`) version tuple.

Python example:

``` py
mtv_cfg: Final = media_type_version.Config(
    log=logging.Logger(...),
    prefix="vnd.acme/thing",
    suffix="+toml",
)

ver_major, ver_minor = media_type_version.extract(mtv_cfg, "vnd.acme/thing.v3.12+toml")
```

Rust example:

``` rust
use media_type_version::{Config as MTVConfig, Error as MTVError, Version as MTVersion};

let cfg = MTVConfig::builder()
    .prefix("vnd.acme/thing")
    .suffix("+toml")
    .build()
    .map_err(MTVError::into_owned_error)?;
assert_eq!(
    media_type_version::extract(&cfg, "vnd.acme/thing.v3.12+toml").as_tuple(),
    (3, 12)
);
```

## The mtv-extract tool

The `media-type-version` library also provides a command-line tool
called `mtv-extract` that will read a series of strings from the specified files,
parse them as media-type strings with the specified prefix and suffix, and
output a line consisting of two tab-separated numbers for each parsed string:

``` sh
$ { echo vnd.acme/thing.v3.47; echo vnd.acme/thing.v42.616; } | mtv-extract -q -p vnd.acme/thing -- -
3       47
42      616
$
```

The `mtv-extract` tool supports the following command-line options:

- `-p prefix` (required): the prefix to strip from the media type string
- `-q`: quiet operation; only display warnings and error messages
- `-s suffix`: the optional suffix to strip from the media type string
- `-v`: verbose operation; display diagnostic output

## Contact

The `media-type-version` library was written by [Peter Pentchev][roam].
It is developed in [a GitLab repository][gitlab].
This documentation is hosted at [Ringlet][ringlet-home] with a copy at [ReadTheDocs][readthedocs].

[roam]: mailto:roam@ringlet.net "Peter Pentchev"
[gitlab]: https://gitlab.com/ppentchev/media-type-version "The media-type-version GitLab repository"
[pypi]: https://pypi.org/project/media-type-version/ "The media-type-version Python Package Index page"
[readthedocs]: https://media-type-version.readthedocs.io/ "The media-type-version ReadTheDocs page"
[ringlet-api-python]: https://devel.ringlet.net/devel/media-type-version/api/python/ "The Python API reference"
[ringlet-home]: https://devel.ringlet.net/devel/media-type-version/ "The Ringlet media-type-version homepage"
