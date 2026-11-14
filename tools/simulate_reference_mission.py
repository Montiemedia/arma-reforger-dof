#!/usr/bin/env python3
"""Simulate a manifest task chain without launching Arma Reforger.

This verifies only the Python reference model, not Enforce runtime behavior.
"""

import argparse
import json
from pathlib import Path
import sys

from dof_task_reference import TaskDirectorCore, TaskResult, TaskState
from validate_mission_manifest import validate_manifest


def simulate(manifest_path: Path) -> int:
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    errors = validate_manifest(data)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    stages = data["stages"]
    director = TaskDirectorCore()

    # AddTask only allows prerequisites that were previously registered.
    # Resolve any valid DAG to deterministic topological registration order.
    remaining = {stage["id"]: stage for stage in stages}
    registered = set()
    ordered = []

    while remaining:
        ready = sorted(
            task_id for task_id, stage in remaining.items()
            if all(dep in registered for dep in stage["depends_on"])
        )
        if not ready:
            print("ERROR: cannot topologically order stages", file=sys.stderr)
            return 1

        for task_id in ready:
            stage = remaining.pop(task_id)
            if not director.add_task(task_id, stage["depends_on"]):
                print(f"ERROR: failed to register {task_id}", file=sys.stderr)
                return 1
            ordered.append(task_id)
            registered.add(task_id)

    if not director.start_mission():
        print("ERROR: failed to start reference mission", file=sys.stderr)
        return 1

    print(f"SIMULATION ONLY: {data['title']} ({data['mission_id']})")

    for task_id in ordered:
        snapshot = director.snapshot(task_id)
        if snapshot is None or snapshot[0] != TaskState.AVAILABLE:
            print(f"ERROR: {task_id} was not unlocked", file=sys.stderr)
            return 1

        state, revision = snapshot
        if director.request_state(task_id, TaskState.ACTIVE, revision) != TaskResult.APPLIED:
            print(f"ERROR: could not activate {task_id}", file=sys.stderr)
            return 1

        if director.request_state(task_id, TaskState.SUCCEEDED, revision + 1) != TaskResult.APPLIED:
            print(f"ERROR: could not complete {task_id}", file=sys.stderr)
            return 1

        print(f"OK: {task_id} AVAILABLE -> ACTIVE -> SUCCEEDED")

    print("SIMULATION COMPLETE (not a Workbench or multiplayer test)")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "manifest",
        type=Path,
        nargs="?",
        default=Path("scenarios/reference_arland/mission.json"),
    )
    sys.exit(simulate(parser.parse_args().manifest))
