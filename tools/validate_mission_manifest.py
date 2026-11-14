#!/usr/bin/env python3
"""Check DOF's *design-only* mission manifests. No Enfusion API is used."""

import argparse
import json
from pathlib import Path
import re
import sys

IDENTIFIER = re.compile(r"^[a-z][a-z0-9_]*$")
TASK_TYPES = {"move", "clear", "defend"}
ACTIVATIONS = {"on_start", "on_predecessors_success"}


def _nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def validate_manifest(document):
    """Return validation errors without modifying the manifest."""
    errors = []
    if not isinstance(document, dict):
        return ["root must be a JSON object"]

    if type(document.get("format_version")) is not int or document["format_version"] != 1:
        errors.append("format_version must be 1")
    if document.get("status") != "design_only":
        errors.append("status must be 'design_only' until an Engine bridge exists")
    if not _nonempty(document.get("mission_id")):
        errors.append("mission_id is required")
    elif not IDENTIFIER.fullmatch(document["mission_id"]):
        errors.append("mission_id must use lower-case snake_case")
    if not _nonempty(document.get("title")):
        errors.append("title is required")
    if document.get("engine") != "Arma Reforger":
        errors.append("engine must be 'Arma Reforger'")
    if document.get("integration") != "scenario_framework":
        errors.append("integration must be 'scenario_framework' in format v1")
    if not _nonempty(document.get("reference_map")):
        errors.append("reference_map is required")

    factions = document.get("factions")
    if not isinstance(factions, dict):
        errors.append("factions must be an object")
    else:
        friendly = factions.get("friendly")
        opposing = factions.get("opposing")
        if not _nonempty(friendly) or not _nonempty(opposing):
            errors.append("factions must have friendly and opposing values")
        elif friendly == opposing:
            errors.append("friendly and opposing factions must differ")

    limits = document.get("limits")
    max_ai = None
    if not isinstance(limits, dict):
        errors.append("limits must be an object")
    else:
        max_ai = limits.get("max_scripted_ai")
        if type(max_ai) is not int or not 1 <= max_ai <= 256:
            errors.append("limits.max_scripted_ai must be an integer from 1 to 256")
        if limits.get("allow_repeat_spawns") is not False:
            errors.append("v1 prototype requires allow_repeat_spawns=false")

    stages = document.get("stages")
    if not isinstance(stages, list) or not 1 <= len(stages) <= 64:
        errors.append("stages must be an array of 1 to 64 entries")
        return errors

    by_id = {}
    layers = set()
    total_slot_count = 0
    for index, stage in enumerate(stages):
        place = f"stages[{index}]"
        if not isinstance(stage, dict):
            errors.append(f"{place} must be an object")
            continue
        stage_id = stage.get("id")
        if not _nonempty(stage_id) or not IDENTIFIER.fullmatch(stage_id):
            errors.append(f"{place}.id must be lower-case snake_case")
        elif stage_id in by_id:
            errors.append(f"duplicate stage id: {stage_id}")
        else:
            by_id[stage_id] = stage

        kind = stage.get("task_type")
        if not isinstance(kind, str) or kind not in TASK_TYPES:
            errors.append(f"{place}.task_type must be one of {sorted(TASK_TYPES)}")
        layer = stage.get("editor_layer")
        slot = stage.get("editor_task_slot")
        if not _nonempty(layer) or not _nonempty(slot):
            errors.append(f"{place} requires editor_layer and editor_task_slot")
        elif layer in layers:
            errors.append(f"duplicate editor_layer: {layer}")
        else:
            layers.add(layer)

        dependencies = stage.get("depends_on")
        if not isinstance(dependencies, list) or any(
            not _nonempty(dependency) for dependency in dependencies
        ):
            errors.append(f"{place}.depends_on must be an array of stage ids")
            dependencies = []
        elif len(set(dependencies)) != len(dependencies):
            errors.append(f"{place}.depends_on contains duplicates")

        expected_activation = (
            "on_start" if not dependencies else "on_predecessors_success"
        )
        if not isinstance(stage.get("activation"), str) or stage.get("activation") != expected_activation:
            errors.append(f"{place}.activation must be {expected_activation}")

        if kind in ("clear", "defend"):
            slots = stage.get("enemy_slots")
            if not isinstance(slots, list) or not slots or any(
                not _nonempty(value) for value in slots
            ):
                errors.append(f"{place}.enemy_slots must be a non-empty array")
            elif len(set(slots)) != len(slots):
                errors.append(f"{place}.enemy_slots contains duplicates")
            else:
                total_slot_count += len(slots)

        if kind == "defend":
            seconds = stage.get("hold_seconds")
            ratio = stage.get("min_defender_ratio")
            if type(seconds) is not int or not 1 <= seconds <= 3600:
                errors.append(f"{place}.hold_seconds must be 1..3600")
            if type(ratio) not in (int, float) or not 0 < ratio <= 1:
                errors.append(f"{place}.min_defender_ratio must be >0 and <=1")

    if type(max_ai) is int and total_slot_count > max_ai:
        errors.append("enemy slot count exceeds limits.max_scripted_ai (conservative preflight)")

    root_count = 0
    for stage_id, stage in by_id.items():
        dependencies = stage.get("depends_on")
        if not isinstance(dependencies, list):
            continue
        if not dependencies:
            root_count += 1
        for dependency in dependencies:
            if dependency not in by_id:
                errors.append(f"{stage_id} depends on unknown stage: {dependency}")
            if dependency == stage_id:
                errors.append(f"{stage_id} cannot depend on itself")

    if root_count != 1:
        errors.append(f"expected exactly one initial stage, got {root_count}")

    seen = set()
    visiting = set()

    def visit(stage_id):
        if stage_id in seen:
            return
        if stage_id in visiting:
            errors.append(f"cycle detected involving {stage_id}")
            return
        visiting.add(stage_id)
        for dependency in by_id[stage_id].get("depends_on", []):
            if isinstance(dependency, str) and dependency in by_id:
                visit(dependency)
        visiting.remove(stage_id)
        seen.add(stage_id)

    for stage_id in by_id:
        visit(stage_id)

    return errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", nargs="+", type=Path)
    options = parser.parse_args(argv)
    failed = False
    for path in options.manifest:
        try:
            with path.open("r", encoding="utf-8") as stream:
                document = json.load(stream)
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            print(f"ERROR {path}: {exc}", file=sys.stderr)
            failed = True
            continue
        errors = validate_manifest(document)
        if errors:
            failed = True
            for error in errors:
                print(f"ERROR {path}: {error}", file=sys.stderr)
        else:
            print(f"OK {path}: manifest preflight passed (NOT an Engine test)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
