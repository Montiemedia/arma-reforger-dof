"""Standard-library unit tests for design-only mission manifests."""

import copy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from validate_mission_manifest import validate_manifest  # noqa: E402


class ManifestValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = ROOT / "scenarios" / "reference_arland" / "mission.json"
        cls.sample = json.loads(path.read_text(encoding="utf-8"))

    def example(self):
        return copy.deepcopy(self.sample)

    def test_reference_manifest_valid(self):
        self.assertEqual([], validate_manifest(self.example()))

    def test_reject_unknown_dependency(self):
        data = self.example()
        data["stages"][1]["depends_on"] = ["does_not_exist"]
        self.assertTrue(any("unknown stage" in s for s in validate_manifest(data)))

    def test_reject_cycle(self):
        data = self.example()
        data["stages"][0]["depends_on"] = ["defend"]
        data["stages"][0]["activation"] = "on_predecessors_success"
        errors = validate_manifest(data)
        self.assertTrue(any("cycle detected" in s for s in errors))

    def test_reject_duplicate_id(self):
        data = self.example()
        data["stages"][1]["id"] = "approach"
        self.assertTrue(any("duplicate stage id" in s for s in validate_manifest(data)))

    def test_reject_bad_defense_ratio(self):
        data = self.example()
        data["stages"][2]["min_defender_ratio"] = 1.5
        self.assertTrue(any("min_defender_ratio" in s for s in validate_manifest(data)))

    def test_reject_repeat_spawn(self):
        data = self.example()
        data["limits"]["allow_repeat_spawns"] = True
        self.assertTrue(any("allow_repeat_spawns" in s for s in validate_manifest(data)))

    def test_reject_over_budget(self):
        data = self.example()
        data["limits"]["max_scripted_ai"] = 1
        self.assertTrue(any("exceeds" in s for s in validate_manifest(data)))

    def test_reject_claim_of_playable(self):
        data = self.example()
        data["status"] = "playable"
        self.assertTrue(any("design_only" in s for s in validate_manifest(data)))


if __name__ == "__main__":
    unittest.main()
