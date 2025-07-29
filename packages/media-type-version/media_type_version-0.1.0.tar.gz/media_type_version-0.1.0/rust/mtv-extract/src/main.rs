#![deny(missing_docs)]
#![deny(clippy::missing_docs_in_private_items)]
// SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
// SPDX-License-Identifier: BSD-2-Clause
//! mtv-extract - read media type strings, extract the format versions from them

use std::fs::File;
use std::io::{self, BufRead as _, BufReader, Error as IoError};

use anyhow::{Context as _, Result, bail};
use argh::FromArgs;
use log::{LevelFilter, info};
use simple_logger::SimpleLogger;

use media_type_version::{Config, Error};

/// Read media type strings, extract the format versions from them.
#[derive(Debug, FromArgs)]
pub struct MtvExtract {
    /// the prefix to expect in the media type string
    #[argh(option, short = 'p')]
    prefix: String,

    /// quiet operation; only display warnings and error messages
    #[argh(switch, short = 'q')]
    quiet: bool,

    /// the optional suffix in the media type string
    #[argh(option, short = 's', default = "String::new()")]
    suffix: String,

    /// verbose operation; display diagnostic messages
    #[argh(switch, short = 'v')]
    verbose: bool,

    /// the files to parse; `-` denotes the standard input stream
    #[argh(positional)]
    files: Vec<String>,
}

/// Read lines from a file, extract the data from them."""
#[expect(clippy::print_stdout, reason = "this is the whole point")]
fn process_lines<L>(cfg: &Config<'_>, fname: &str, lines: L) -> Result<()>
where
    L: Iterator<Item = Result<String, IoError>>,
{
    for line_res in lines {
        let line = line_res.with_context(|| format!("Could not read a line from {fname}"))?;
        let ver = media_type_version::extract(cfg, &line)
            .map_err(Error::into_owned_error)
            .with_context(|| format!("Could not parse a line read from {fname}: {line}"))?;
        println!("{major}\t{minor}", major = ver.major(), minor = ver.minor());
    }
    Ok(())
}

fn main() -> Result<()> {
    let args: MtvExtract = argh::from_env();
    if args.files.is_empty() {
        bail!("No files to process");
    }
    SimpleLogger::new()
        .with_level(if args.verbose {
            LevelFilter::Trace
        } else if args.quiet {
            LevelFilter::Warn
        } else {
            LevelFilter::Info
        })
        .init()
        .context("Could not set up logging")?;

    let cfg = Config::builder()
        .prefix(&args.prefix)
        .suffix(&args.suffix)
        .build()
        .map_err(Error::into_owned_error)
        .context("Could not build the MTConfig")?;
    for fname in args.files {
        if fname == "-" {
            info!("Reading from the standard input");
            process_lines(&cfg, "(standard input)", io::stdin().lines())?;
        } else {
            info!("Reading from the {fname} file");
            let infile = File::open(&fname)
                .with_context(|| format!("Could not open the {fname} file for reading"))?;
            process_lines(&cfg, &fname, BufReader::new(infile).lines())?;
        }
    }
    Ok(())
}
