#!/usr/bin/env python3
"""Explicitly stage a locally installed QF-Test manual for offline transfer.

Run only if you are authorized to copy/transfer the vendor documentation.
Never downloads files. Refuses symlinks and an existing destination.
"""

import argparse
import pathlib
import shutil
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("installed_manual", type=pathlib.Path,
                        help="the QF-Test 11.0.0 doc/manual/en directory")
    parser.add_argument("--authorized-to-copy", action="store_true",
                        help="confirm you have permission to transfer this manual")
    args = parser.parse_args()
    if not args.authorized_to_copy:
        parser.error("pass --authorized-to-copy only when your terms permit transfer")
    source = args.installed_manual
    target = pathlib.Path(__file__).resolve().parent.parent / "vendor-docs" / "manual" / "en"
    if not source.is_dir() or not (source / "contents.html").is_file():
        parser.error("expected a local doc/manual/en directory with contents.html")
    if target.exists():
        parser.error("destination already exists; inspect it before replacing anything")
    if any(path.is_symlink() for path in (source, *source.rglob("*"))):
        parser.error("refusing symlinks in the manual tree")
    shutil.copytree(source, target)
    print("Staged manual at", target)
    print("Verify it is the installed 11.0.0 manual before transferring.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
