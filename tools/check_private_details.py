"""Fail when a tracked file names a contributor's machine.

The repository is public. Private network hostnames and local home-directory
paths identify a person and their machine, and mean nothing to a reader.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PRIVATE = {
    "Tailscale hostname": re.compile(r"[A-Za-z0-9-]+\.ts\.net\b"),
    "macOS home directory": re.compile(r"/Users/[A-Za-z]"),
    "Linux home directory": re.compile(r"/home/[a-z_][a-z0-9_-]*/"),
    "agent profile directory": re.compile(r"\.hermes[/\\]"),
}


def tracked() -> list[Path]:
    listed = subprocess.run(
        ["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, check=True
    ).stdout.decode()
    return [ROOT / name for name in listed.split("\0") if name]


def offenders() -> list[str]:
    found = []
    for path in tracked():
        try:
            data = path.read_bytes()
        except OSError:
            continue
        if b"\0" in data[:8192]:
            continue
        text = data.decode("utf-8", errors="replace")
        for number, line in enumerate(text.splitlines(), 1):
            for kind, pattern in PRIVATE.items():
                if pattern.search(line):
                    found.append(f"{path.relative_to(ROOT).as_posix()}:{number}: {kind}")
    return found


def main() -> int:
    found = offenders()
    if found:
        print("Remove private details from:", *found, sep="\n", file=sys.stderr)
        return 1
    print("No private hostnames or home directories in tracked files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
