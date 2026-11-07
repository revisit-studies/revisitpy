"""Set a release version without rewriting unrelated pyproject.toml content."""

import argparse
from pathlib import Path
import re
import tomllib


def parse_version(version: str) -> tuple[int, int, int]:
    """Accept canonical, non-negative X.Y.Z versions only."""
    if not isinstance(version, str) or not re.fullmatch(
        r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)", version
    ):
        raise ValueError(f"Expected a canonical X.Y.Z version, got {version!r}")
    return tuple(int(part) for part in version.split("."))


def select_version(current: str, bump: str, version: str = "") -> str:
    current_parts = parse_version(current)
    if bump not in ("patch", "minor"):
        raise ValueError(f"Unsupported version bump: {bump!r}")
    if version.strip():
        requested = parse_version(version)
        if requested < current_parts:
            raise ValueError(f"Cannot downgrade from {current} to {version}")
        # An explicit equal version allows retrying a failed publication without
        # advancing the version again. PyPI still rejects duplicate artifacts.
        return version
    major, minor, patch = current_parts
    return f"{major}.{minor}.{patch + 1}" if bump == "patch" else f"{major}.{minor + 1}.0"


def select_study_version(current: str, study_tag: str, version: str = "") -> str:
    """Follow the study's major/minor while allowing independent package patches."""
    if not study_tag.startswith("v"):
        raise ValueError("Study release tag must have the form vX.Y.Z")
    study = parse_version(study_tag[1:])
    package = parse_version(current)
    if study[:2] < package[:2]:
        raise ValueError("Cannot publish an older study major/minor series")
    if version:
        requested = parse_version(version)
        if requested[:2] != study[:2]:
            raise ValueError("Package major/minor must match the study release")
        return select_version(current, "patch", version)
    if study[:2] == package[:2]:
        return f"{package[0]}.{package[1]}.{package[2] + 1}"
    return f"{study[0]}.{study[1]}.0"


def update_project_version(project: Path, bump: str, version: str = "", study_tag: str = "") -> str:
    """Validate before writing; preserve every byte outside the version value."""
    source = project.read_bytes().decode("utf-8")
    document = tomllib.loads(source)
    current = document.get("project", {}).get("version")
    new_version = (select_study_version(current, study_tag, version)
                   if study_tag else select_version(current, bump, version))
    # Restrict the edit to an ordinary [project] table and a single-line version
    # assignment. Reject unsupported layouts rather than risking another table.
    table = re.search(r"(?m)^\[project\][ \t]*(?:#[^\r\n]*)?\r?$", source)
    if table is None:
        raise ValueError("Cannot locate the [project] table")
    next_table = re.search(r"(?m)^[ \t]*\[", source[table.end():])
    end = table.end() + next_table.start() if next_table else len(source)
    assignments = list(re.finditer(
        r"(?m)^[ \t]*version[ \t]*=[ \t]*([\"'])([^\r\n]*?)\1[ \t]*(?:#[^\r\n]*)?\r?$",
        source[table.end():end],
    ))
    if len(assignments) != 1 or assignments[0].group(2) != current:
        raise ValueError("Expected one single-line version assignment in [project]")
    assignment = assignments[0]
    start = table.end() + assignment.start(2)
    stop = table.end() + assignment.end(2)
    updated = source[:start] + new_version + source[stop:]
    expected = document.copy()
    expected["project"] = dict(document["project"], version=new_version)
    if tomllib.loads(updated) != expected:
        raise ValueError("Version edit would change unrelated project data")
    if updated != source:
        project.write_bytes(updated.encode("utf-8"))
    return new_version


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, default=Path("pyproject.toml"))
    parser.add_argument("--bump", choices=("patch", "minor"), required=True)
    parser.add_argument("--version", default="", help="Exact X.Y.Z version; blank uses --bump")
    parser.add_argument("--study-tag", default="", help="Study release tag vX.Y.Z")
    args = parser.parse_args()
    try:
        version = update_project_version(args.project, args.bump, args.version, args.study_tag)
    except (ValueError, OSError) as error:
        parser.exit(1, f"Error: {error}\n")
    print(version)


if __name__ == "__main__":
    main()
