#!/usr/bin/env python3
"""Validate fictional DOF mission story catalogs, NOT Arma Reforger gameplay.

Each of the four perspective catalogs must have 200 complete, nonduplicated
mission drafts. All data remains narrative design content, not Engine resources.
"""

from collections import Counter
from pathlib import Path
import argparse
import json
import sys

FACTIONS = ("US", "USSR", "FIA", "CIV")
TYPES = {
    "defend", "deliver", "escort", "evacuate", "investigate",
    "medical", "negotiate", "patrol", "recon", "recover",
    "repair", "rescue", "secure"
}
STORY_KEYS = (
    "premise", "personal_context", "initial_briefing", "turning_point",
    "human_stakes", "success_epilogue", "failure_epilogue"
)
CATEGORIES = 20


def load_seeds(path: Path):
    """Read human-authored source seeds with explicit column/count checking."""
    problems = []
    plots = []
    group = ""
    for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        raw = raw.strip()
        if not raw:
            continue
        if raw.startswith("# "):
            if not raw.startswith(("# DOF", "# Fictional", "# Format")):
                group = raw[2:].strip()
            continue
        if raw.startswith("#"):
            continue
        cols = [cell.strip() for cell in raw.split("|")]
        if len(cols) != 8 or any(not x for x in cols):
            problems.append(f"{path}:{line_number}: expected eight nonblank fields")
            continue
        plots.append({"category": group, "title": cols[0], "incident": cols[1],
                      "objective": cols[2], "reveal": cols[3], "choice_a": cols[4], "choice_b": cols[5], "type": cols[7]})
    if len(plots) != 200:
        problems.append(f"story seeds: expected 200, found {len(plots)}")
    if len(set(p["title"] for p in plots)) != len(plots):
        problems.append("story seeds: duplicate titles")
    if len(set(p["category"] for p in plots)) != CATEGORIES:
        problems.append(f"story seeds: expected {CATEGORIES} categories")
    return plots, problems


def text(value, minimum=8):
    return isinstance(value, str) and len(value.strip()) >= minimum


def validate_catalog(document, faction, plots):
    errors = []
    if not isinstance(document, dict):
        return ["catalog must be an object"]
    if document.get("library_format") != 1 or document.get("design_only") is not True:
        errors.append("catalog must declare format=1 and design_only=true")
    if document.get("playable_faction") != faction:
        errors.append("wrong playable faction")
    if document.get("count") != 200:
        errors.append("count metadata must be 200")
    if document.get("source_seed_file") != "content/story_seeds_v1.txt":
        errors.append("wrong story seed reference")
    items = document.get("scenarios")
    if not isinstance(items, list):
        return errors + ["scenarios must be a list"]
    if len(items) != 200:
        errors.append(f"{faction}: expected 200 scenarios, got {len(items)}")

    ids = set()
    plot_ids = set()
    people = set()
    categories = set()
    types = set()
    for index, m in enumerate(items):
        label = f"{faction}[{index+1:03}]"
        if not isinstance(m, dict):
            errors.append(f"{label} must be object")
            continue
        expected_id = f"dof_{faction.lower()}_{index+1:03}"
        expected_plot = f"plot_{index+1:03}"
        if m.get("id") != expected_id or m.get("id") in ids:
            errors.append(f"{label}: invalid or duplicate id")
        ids.add(m.get("id"))
        if m.get("plot_id") != expected_plot or m.get("plot_id") in plot_ids:
            errors.append(f"{label}: invalid or duplicate plot id")
        plot_ids.add(m.get("plot_id"))
        if m.get("faction") != faction or m.get("playable_coop") is not True:
            errors.append(f"{label}: faction/coop mismatch")
        if m.get("mission_status") != "narrative_design_only":
            errors.append(f"{label}: unverified playable claim")
        if not text(m.get("title")):
            errors.append(f"{label}: missing title")

        if index < len(plots):
            plot = plots[index]
            if plot["title"] not in m.get("title", ""):
                errors.append(f"{label}: seed title missing")
            if m.get("category") != plot["category"]:
                errors.append(f"{label}: seed category mismatch")
            if m.get("mission_type") != plot["type"]:
                errors.append(f"{label}: seed task type mismatch")
            if m.get("objectives", {}).get("primary") != plot["objective"]:
                errors.append(f"{label}: primary objective diverges from seed")
            if plot["incident"] not in m.get("story", {}).get("premise", ""):
                errors.append(f"{label}: unique story incident missing")
            if plot["reveal"] not in m.get("story", {}).get("turning_point", ""):
                errors.append(f"{label}: plot twist missing")
        categories.add(m.get("category"))
        types.add(m.get("mission_type"))
        if m.get("mission_type") not in TYPES:
            errors.append(f"{label}: unknown mission type")
        story = m.get("story")
        if not isinstance(story, dict) or any(
            not text(story.get(k), 8 if k == "human_stakes" else 20)
            for k in STORY_KEYS
        ):
            errors.append(f"{label}: incomplete story or epilogue")
        chars = m.get("characters")
        if not isinstance(chars, list) or len(chars) < 2:
            errors.append(f"{label}: requires two characters")
        else:
            for c in chars:
                if not isinstance(c, dict) or not text(c.get("name")) or not text(c.get("role")) or not text(c.get("personal_stakes"), 15):
                    errors.append(f"{label}: character requires name, role, motivation")
                    continue
                if c["name"] in people:
                    errors.append(f"{label}: duplicate character {c['name']}")
                people.add(c["name"])
        o = m.get("objectives")
        if not isinstance(o, dict) or not text(o.get("primary")) or len(o.get("secondary", [])) < 1 or len(o.get("success_conditions", [])) < 1 or len(o.get("failure_conditions", [])) < 1:
            errors.append(f"{label}: incomplete mission objectives")
        choices = m.get("choices")
        if not isinstance(choices, list) or len(choices) != 2 or not all(
            isinstance(c, dict) and text(c.get("action")) and text(c.get("consequence"), 25)
            for c in choices
        ):
            errors.append(f"{label}: two complete decision branches required")
        else:
            if choices[0]["action"] == choices[1]["action"]:
                errors.append(f"{label}: choice actions must differ")
            if index < len(plots) and (
                choices[0]["action"] != plots[index]["choice_a"]
                or choices[1]["action"] != plots[index]["choice_b"]
            ):
                errors.append(f"{label}: choice actions do not match source story")
            if any("undefined" in c["consequence"].lower() for c in choices):
                errors.append(f"{label}: undefined placeholder in choice consequences")

        events = m.get("dynamic_events")
        if not isinstance(events, list) or len(events) < 2 or not all(isinstance(e, dict) and text(e.get("event")) and text(e.get("trigger")) for e in events):
            errors.append(f"{label}: missing dynamic events")
        civilians = m.get("civilian_life")
        if not isinstance(civilians, dict) or civilians.get("optional") is not True or civilians.get("civilian_harm_avoidance") is not True:
            errors.append(f"{label}: civilian-life protections missing")
        policy = m.get("faction_policy")
        if not isinstance(policy, dict):
            errors.append(f"{label}: missing faction policy")
        else:
            if policy.get("playable_faction_alias") != "DOF_FRIENDLY":
                errors.append(f"{label}: player alias missing")
            if policy.get("runtime_faction_switch_allowed") is not False:
                errors.append(f"{label}: runtime faction switches forbidden")
            if policy.get("faction_key_verified") is not False:
                errors.append(f"{label}: engine faction-key verification falsely claimed")
            if faction == "CIV" and (policy.get("opposing_faction_alias") is not None or policy.get("weapons_mandatory") is not False):
                errors.append(f"{label}: civilian missions cannot require weapons or opposing military factions")
        setting = m.get("setting", {})
        if not isinstance(setting, dict) or setting.get("world_binding") != "map_agnostic":
            errors.append(f"{label}: no map-agnostic setting")
        impl = m.get("implementation", {})
        if not isinstance(impl, dict) or impl.get("engine_assets") != "not_created" or impl.get("workbench_compile") != "not_tested" or impl.get("mission_module") != "not_implemented":
            errors.append(f"{label}: false implementation status")
    if len(categories) != CATEGORIES:
        errors.append(f"{faction}: expected {CATEGORIES} categories")
    if len(types) < 12:
        errors.append(f"{faction}: expected >=12 mission types, got {len(types)}")
    return errors


def validate_library(directory: Path, seed_path: Path):
    try:
        plots, problems = load_seeds(seed_path)
    except (OSError, UnicodeError) as error:
        return [f"could not read story seeds: {error}"]
    all_ids = set()
    for faction in FACTIONS:
        path = directory / f"{faction.lower()}.json"
        try:
            document = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as error:
            problems.append(f"{path}: {error}")
            continue
        problems.extend(validate_catalog(document, faction, plots))
        for entry in document.get("scenarios", []):
            if isinstance(entry, dict):
                id_value = entry.get("id")
                if id_value in all_ids:
                    problems.append(f"global duplicate mission id: {id_value}")
                all_ids.add(id_value)
    if len(all_ids) != 800:
        problems.append(f"expected 800 unique global ids, got {len(all_ids)}")
    return problems


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path, nargs="?", default=Path("content/missions"))
    parser.add_argument("--seeds", type=Path, default=Path("content/story_seeds_v1.txt"))
    args = parser.parse_args()
    problems = validate_library(args.directory, args.seeds)
    if problems:
        for problem in problems:
            print("ERROR:", problem, file=sys.stderr)
        return 1
    print("OK: 800 narrative mission drafts, 200 per faction, 20 story domains")
    print("NOT AN ARMA REFORGER ENGINE / WORKBENCH / MULTIPLAYER TEST")
    return 0


if __name__ == "__main__":
    sys.exit(main())
