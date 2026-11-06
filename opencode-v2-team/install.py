#!/usr/bin/env python3
"""Render the team config with this checkout's absolute skill paths."""

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shutil
import tempfile

from verify_setup import ProbeError, validate


PACKAGE = Path(__file__).resolve().parent
SKILLS_VARIABLE = "{env:OPENCODE_SKILLS_DIR}"


def render(skills_dir):
    root = skills_dir.expanduser().resolve(strict=True)
    if any(char in root.as_posix() for char in ("*", "?")):
        raise ValueError("The skills path must not contain permission wildcard characters (* or ?).")
    approved = json.loads((PACKAGE / "skills.json").read_text(encoding="utf-8"))
    for skill_id, relative in approved.items():
        folder = (root / relative).resolve(strict=True)
        if not folder.is_relative_to(root) or folder.name != skill_id:
            raise ValueError(f"Unexpected path or path-derived skill ID: {skill_id}")
        if folder != root / relative:
            raise ValueError(f"Symlinked skill directories need explicit canonical permission paths: {skill_id}")
        if not (folder / "SKILL.md").is_file():
            raise ValueError(f"Missing skill entry point: {skill_id}")
    template = json.loads((PACKAGE / "opencode.jsonc").read_text(encoding="utf-8"))

    def replace(value):
        if isinstance(value, str):
            return value.replace(SKILLS_VARIABLE, root.as_posix())
        if isinstance(value, dict):
            return {key: replace(item) for key, item in value.items()}
        if isinstance(value, list):
            return [replace(item) for item in value]
        return value

    return replace(template)


def write_config(config, destination, replace_existing=False):
    target = destination.expanduser().absolute()
    if target.resolve() == (PACKAGE / "opencode.jsonc").resolve():
        raise ValueError("Choose an installed/preview path; do not overwrite the portable source template.")
    if target.suffix not in (".json", ".jsonc"):
        raise ValueError("Choose a .json or .jsonc output path.")
    if target.is_symlink():
        raise ValueError("Refusing to replace a symlink; select its intended destination explicitly.")
    alternate = target.with_suffix(".json" if target.suffix == ".jsonc" else ".jsonc")
    if alternate.exists():
        raise ValueError(f"Alternate config already exists: {alternate}. Choose that file to avoid conflicting configs.")
    if target.exists() and not replace_existing:
        raise ValueError("Output already exists. Use --replace to save a backup and replace the full config, or choose a new preview path.")
    target.parent.mkdir(parents=True, exist_ok=True)
    backup = None
    if target.exists():
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        backup = target.with_name(target.name + ".bak-" + stamp)
        shutil.copy2(target, backup)
    descriptor, temporary = tempfile.mkstemp(prefix=".opencode-team-", dir=target.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(config, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
        # For a new file, exclusive creation also protects against a concurrent installer.
        if replace_existing:
            os.replace(temporary, target)
        else:
            with target.open("x", encoding="utf-8") as handle:
                handle.write(Path(temporary).read_text(encoding="utf-8"))
    finally:
        Path(temporary).unlink(missing_ok=True)
    return target, backup


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--check", action="store_true", help="Render and validate in memory without writing anything.")
    action.add_argument("--output", type=Path, help="Write a full rendered config to this exact path.")
    parser.add_argument("--skills-dir", type=Path, default=PACKAGE.parent, help="Skills repository checkout; defaults to the parent of this package.")
    parser.add_argument("--replace", action="store_true", help="Back up and replace an existing output; does not merge settings.")
    args = parser.parse_args()
    if args.replace and not args.output:
        parser.error("--replace requires --output.")
    try:
        config = render(args.skills_dir)
        validate(config)
        if args.output:
            target, backup = write_config(config, args.output, args.replace)
            print(f"Wrote full team configuration: {target}")
            if backup:
                print(f"Previous configuration backed up: {backup}")
        else:
            print("PASS: approved skills exist; all paths render without writing a target config.")
        print("The API-key environment reference is preserved; no credentials were read or written.")
        return 0
    except (ProbeError, OSError, ValueError, KeyError, StopIteration, TypeError) as exc:
        print(f"FAIL: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
