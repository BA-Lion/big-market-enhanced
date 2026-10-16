"""Validate the structure and lightweight metadata contract of `.ai`."""

from __future__ import annotations

import re
import sys
from pathlib import Path


AI_ROOT = Path(__file__).resolve().parents[2]

REQUIRED_FILES = {
    "readme.md",
    "index.md",
    "project.md",
    "templates/architecture.md",
    "templates/attention.md",
    "templates/decision.md",
    "templates/doc.md",
    "templates/implementation.md",
    "templates/problem.md",
    "templates/task-current.md",
    "templates/task-future.md",
    "templates/test-experience.md",
    "templates/test-result.md",
}

REQUIRED_DIRECTORIES = {
    "architecture",
    "attention",
    "decision",
    "doc",
    "implementation",
    "problem",
    "task/current",
    "task/future",
    "templates",
    "test/experience",
    "test/result",
    "test/script",
}

FORBIDDEN_LEGACY_DIRECTORIES = {"decison", "implemention"}

RECORD_RULES = {
    "architecture": (
        "architecture",
        {"proposed", "accepted", "superseded", "deprecated"},
    ),
    "attention": ("attention", {"verified", "provisional", "obsolete"}),
    "decision": (
        "decision",
        {"draft", "approved", "rejected", "superseded", "cancelled"},
    ),
    "doc": ("module-doc", {"current", "provisional", "obsolete"}),
    "implementation": (
        "implementation",
        {
            "draft",
            "approved",
            "in_progress",
            "blocked",
            "completed",
            "superseded",
            "cancelled",
        },
    ),
    "problem": (
        "problem",
        {"open", "investigating", "mitigated", "resolved", "accepted"},
    ),
    "task/current": (
        "task",
        {"planned", "active", "blocked", "completed", "cancelled"},
    ),
    "task/future": ("future-task", {"deferred", "promoted", "cancelled"}),
    "test/experience": (
        "test-experience",
        {"verified", "provisional", "obsolete"},
    ),
    "test/result": ("test-result", {"passed", "failed", "partial", "blocked"}),
}

LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")


def relative(path: Path) -> str:
    return path.relative_to(AI_ROOT).as_posix()


def parse_front_matter(path: Path) -> tuple[dict[str, str] | None, str | None]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return None, "missing opening front matter delimiter"

    try:
        end = lines.index("---", 1)
    except ValueError:
        return None, "missing closing front matter delimiter"

    values: dict[str, str] = {}
    for line in lines[1:end]:
        if not line or line.startswith((" ", "\t", "#")) or ":" not in line:
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip("'\"")
    return values, None


def iter_record_files(directory: str):
    base = AI_ROOT / directory
    if not base.exists():
        return
    for path in base.rglob("*.md"):
        if "archive" not in path.parts:
            yield path


def check_relative_links(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    for raw_target in LINK_RE.findall(text):
        target = raw_target.strip().split("#", 1)[0]
        if not target or "://" in target or target.startswith(("#", "mailto:")):
            continue
        target = target.strip("<>")
        if not (path.parent / target).resolve().exists():
            errors.append(f"{relative(path)}: broken relative link: {raw_target}")
    return errors


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    for item in sorted(REQUIRED_FILES):
        if not (AI_ROOT / item).is_file():
            errors.append(f"missing required file: {item}")

    for item in sorted(REQUIRED_DIRECTORIES):
        if not (AI_ROOT / item).is_dir():
            errors.append(f"missing required directory: {item}")

    for item in sorted(FORBIDDEN_LEGACY_DIRECTORIES):
        if (AI_ROOT / item).exists():
            errors.append(f"legacy misspelled directory still exists: {item}")

    for directory, (expected_type, statuses) in RECORD_RULES.items():
        for path in iter_record_files(directory) or ():
            values, parse_error = parse_front_matter(path)
            if parse_error:
                errors.append(f"{relative(path)}: {parse_error}")
                continue
            assert values is not None
            if values.get("type") != expected_type:
                errors.append(
                    f"{relative(path)}: type must be {expected_type!r}, "
                    f"got {values.get('type')!r}"
                )
            if values.get("status") not in statuses:
                errors.append(
                    f"{relative(path)}: invalid status {values.get('status')!r}; "
                    f"allowed: {', '.join(sorted(statuses))}"
                )
            for key in ("id", "created", "updated"):
                if not values.get(key):
                    errors.append(f"{relative(path)}: missing required metadata: {key}")

    for path in AI_ROOT.rglob("*.md"):
        if path.parent != AI_ROOT / "templates":
            errors.extend(check_relative_links(path))

    project_text = (AI_ROOT / "project.md").read_text(encoding="utf-8")
    if "status: uninitialized" in project_text or "TBD" in project_text:
        warnings.append("project.md is not initialized; replace all TBD values before use")

    for warning in warnings:
        print(f"WARN: {warning}")
    for error in errors:
        print(f"ERROR: {error}")

    if errors:
        print(f"FAIL: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1

    print(f"PASS: .ai harness is structurally valid ({len(warnings)} warning(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
