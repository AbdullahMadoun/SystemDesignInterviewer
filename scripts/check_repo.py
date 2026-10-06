#!/usr/bin/env python3
"""
Repository hygiene checks. Run locally before pushing and in CI.

Fails if:
  * SKILL.md frontmatter is missing or invalid (name / description).
  * Any file referenced from SKILL.md does not exist.
  * Personal state (candidate_profile.md, history/) is tracked by git.
  * Tracked files contain absolute user paths or Excalidraw room keys.
  * Tracked text files use CRLF line endings.
  * Python scripts fail to compile.
"""

from __future__ import annotations

import pathlib
import py_compile
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
errors: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)


def tracked_files() -> list[pathlib.Path]:
    try:
        out = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard"],
                             cwd=ROOT, capture_output=True, text=True, check=True).stdout
        return [ROOT / f for f in out.splitlines() if f and (ROOT / f).is_file()]
    except (subprocess.CalledProcessError, FileNotFoundError):
        return [p for p in ROOT.rglob("*") if p.is_file() and ".git" not in p.parts]


def check_frontmatter() -> None:
    skill = ROOT / "SKILL.md"
    if not skill.exists():
        return fail("SKILL.md is missing")
    text = skill.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return fail("SKILL.md: missing YAML frontmatter")
    fm = dict(re.findall(r"^(\w+):\s*(.+)$", m.group(1), re.M))
    name = fm.get("name", "")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name) or len(name) > 64:
        fail(f"SKILL.md: invalid name {name!r} (lowercase-hyphenated, <= 64 chars)")
    desc = fm.get("description", "")
    if not desc or len(desc) > 1024:
        fail(f"SKILL.md: description must be 1-1024 chars (got {len(desc)})")
    for ref in sorted(set(re.findall(r"`((?:scripts|references|templates)/[\w./-]+)`", text))):
        if not (ROOT / ref).exists():
            fail(f"SKILL.md references missing file: {ref}")


def check_files(files: list[pathlib.Path]) -> None:
    rels = {f.relative_to(ROOT).as_posix() for f in files}
    for forbidden in ("candidate_profile.md",):
        if forbidden in rels:
            fail(f"personal file would be published: {forbidden}")
    if any(r.startswith("history/") for r in rels):
        fail("personal board history would be published: history/")

    patterns = {
        "absolute user path": re.compile(r"(/Users/[A-Za-z0-9_.-]+|/home/[A-Za-z0-9_.-]+|C:\\\\Users\\\\)"),
        "Excalidraw room key": re.compile(r"#room=[A-Za-z0-9]{8,},[A-Za-z0-9_-]{8,}"),
    }
    for f in files:
        if f.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".ico"}:
            continue
        rel = f.relative_to(ROOT).as_posix()
        if rel == "scripts/check_repo.py":
            continue
        raw = f.read_bytes()
        if b"\r\n" in raw:
            fail(f"{rel}: CRLF line endings")
        text = raw.decode("utf-8", errors="replace")
        for label, pat in patterns.items():
            if pat.search(text):
                fail(f"{rel}: contains {label}")
        if f.suffix == ".py":
            try:
                py_compile.compile(str(f), doraise=True, cfile=None)
            except py_compile.PyCompileError as exc:
                fail(f"{rel}: does not compile: {exc.msg}")


def main() -> int:
    check_frontmatter()
    check_files(tracked_files())
    if errors:
        print("Repository checks FAILED:")
        for e in errors:
            print(f"  ✗ {e}")
        return 1
    print("Repository checks passed ✓")
    return 0


if __name__ == "__main__":
    sys.exit(main())
