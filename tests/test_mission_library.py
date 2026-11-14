"""Regression checks for the four fictional 200-mission catalogs."""

import copy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from validate_mission_library import load_seeds, validate_catalog, validate_library


class LibraryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plots, cls.problems = load_seeds(ROOT / "content/story_seeds_v1.txt")
        cls.catalogs = {
            faction: json.loads((ROOT / "content/missions" / f"{faction.lower()}.json").read_text(encoding="utf-8"))
            for faction in ("US", "USSR", "FIA", "CIV")
        }

    def test_all_800_missions_validate(self):
        self.assertEqual([], validate_library(ROOT / "content/missions", ROOT / "content/story_seeds_v1.txt"))

    def test_exactly_200_seeds(self):
        self.assertEqual([], self.problems)
        self.assertEqual(200, len(self.plots))

    def test_all_mission_ids_unique(self):
        ids = [m["id"] for c in self.catalogs.values() for m in c["scenarios"]]
        self.assertEqual(800, len(set(ids)))

    def test_each_faction_has_200_named_stories(self):
        for faction, doc in self.catalogs.items():
            with self.subTest(faction=faction):
                self.assertEqual(200, len(doc["scenarios"]))
                self.assertEqual(400, sum(len(m["characters"]) for m in doc["scenarios"]))
                self.assertEqual([], validate_catalog(doc, faction, self.plots))

    def test_civilian_no_mandatory_weapons(self):
        for m in self.catalogs["CIV"]["scenarios"]:
            self.assertFalse(m["faction_policy"]["weapons_mandatory"])
            self.assertIsNone(m["faction_policy"]["opposing_faction_alias"])

    def test_reject_duplicate_mission(self):
        sample = copy.deepcopy(self.catalogs["US"])
        sample["scenarios"][1]["id"] = sample["scenarios"][0]["id"]
        self.assertTrue(any("duplicate id" in e for e in validate_catalog(sample, "US", self.plots)))

    def test_reject_missing_story(self):
        sample = copy.deepcopy(self.catalogs["FIA"])
        del sample["scenarios"][4]["story"]["turning_point"]
        self.assertTrue(any("incomplete story" in e for e in validate_catalog(sample, "FIA", self.plots)))

    def test_reject_missing_character(self):
        sample = copy.deepcopy(self.catalogs["USSR"])
        sample["scenarios"][0]["characters"] = []
        self.assertTrue(any("requires two characters" in e for e in validate_catalog(sample, "USSR", self.plots)))

    def test_reject_fake_playable_status(self):
        sample = copy.deepcopy(self.catalogs["CIV"])
        sample["scenarios"][3]["implementation"]["workbench_compile"] = "passed"
        self.assertTrue(any("false implementation status" in e for e in validate_catalog(sample, "CIV", self.plots)))


if __name__ == "__main__":
    unittest.main()
