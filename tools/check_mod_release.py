#!/usr/bin/env python3
"""Check *declared* requirements for a DOF Workbench mod release.

Does not compile Enforce, bundle assets, validate game logic or publish a mod.
Exit 1 if required native resources or QA attestations are missing.
"""
import argparse
import json
from pathlib import Path
import sys

STAGES = {
    "local-alpha": ("workbench_compile", "local_play"),
    "publish-candidate": ("workbench_compile", "local_play", "listen_server", "dedicated_server", "bundle"),
}
ALPHA_BASE = Path("addon/DOF_DynamicOperations")


def _present_text(value):
    return isinstance(value, str) and bool(value.strip())


def _assets_under(root, folder, extension):
    return sorted(
        p for p in root.rglob("*")
        if p.is_file()
        and p.suffix.lower() == extension
        and folder.lower() in (part.lower() for part in p.relative_to(root).parts[:-1])
    )


def check_release(addon_root, stage="local-alpha", evidence_path=None):
    """Return a list of blockers, never modifying local files."""
    blockers = []
    if stage not in STAGES:
        return [f"unknown stage: {stage}"]
    addon_root = Path(addon_root)
    if not addon_root.is_dir():
        return [f"Workbench addon directory missing: {addon_root}"]

    projects = sorted(addon_root.glob("*.gproj"))
    if len(projects) != 1:
        blockers.append("Expected exactly one Workbench-generated *.gproj in addon root.")

    worlds = _assets_under(addon_root, "worlds", ".ent")
    if not worlds:
        blockers.append("No Workbench-generated .ent world beneath worlds/.")
    headers = _assets_under(addon_root, "missions", ".conf")
    if not headers:
        blockers.append("No Workbench-generated .conf mission header beneath Missions/.")

    for resource in worlds + headers:
        meta = Path(str(resource) + ".meta")
        if not meta.is_file():
            blockers.append(f"Resource metadata missing: {meta.relative_to(addon_root)}")

    if evidence_path is None:
        evidence_path = addon_root / "release" / "qa-evidence.json"
    evidence_path = Path(evidence_path)
    if not evidence_path.is_file():
        blockers.append(f"QA evidence missing: {evidence_path}")
        return blockers

    try:
        record = json.loads(evidence_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        blockers.append(f"Cannot read QA evidence: {exc}")
        return blockers

    if not isinstance(record, dict) or record.get("schema_version") != 1:
        blockers.append("QA evidence schema_version must be 1.")
        return blockers

    for field in ("reforger_version", "workbench_version", "scenario_name"):
        if not _present_text(record.get(field)):
            blockers.append(f"QA evidence missing nonblank {field}.")

    checks = record.get("checks", {})
    if not isinstance(checks, dict):
        blockers.append("QA evidence checks must be an object.")
        return blockers
    for check_name in STAGES[stage]:
        check = checks.get(check_name)
        if (not isinstance(check, dict)
                or check.get("passed") is not True
                or not _present_text(check.get("evidence"))):
            blockers.append(
                f"QA test {check_name} must be marked passed with a nonblank log/report reference."
            )
    return blockers


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--addon-root", type=Path, default=ALPHA_BASE,
        help="Workbench-generated addon directory (default: addon/DOF_DynamicOperations)"
    )
    parser.add_argument(
        "--stage", choices=sorted(STAGES), default="local-alpha",
        help="Gate for local alpha or a candidate for publishing"
    )
    parser.add_argument(
        "--evidence", type=Path, default=None,
        help="Optional QA evidence JSON (default: <addon-root>/release/qa-evidence.json)"
    )
    args = parser.parse_args(argv)
    errors = check_release(args.addon_root, args.stage, args.evidence)
    if errors:
        print("DOF MOD NOT READY (this is a local file/attestation check):")
        for error in errors:
            print(" - " + error)
        return 1
    print("DOF FILE/ATTESTATION GATE PASSED.")
    print("IMPORTANT: This script CANNOT independently prove Workbench compilation,")
    print("multiplayer correctness, actual bundle integrity, or Workshop availability.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
