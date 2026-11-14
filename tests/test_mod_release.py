"""Tests for the DOF release readiness *preflight*, not the Reforger engine."""
from pathlib import Path
import json
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from check_mod_release import check_release


def write_fixture(root):
    (root / "addon.gproj").write_text("Workbench-generated project placeholder for unit tests", encoding="utf-8")
    world = root / "worlds" / "DOF_Arland" / "DOF_Arland.ent"
    world.parent.mkdir(parents=True)
    world.write_text("unit test only", encoding="utf-8")
    Path(str(world) + ".meta").write_text("unit test only", encoding="utf-8")
    header = root / "Missions" / "DOF_Arland.conf"
    header.parent.mkdir(parents=True)
    header.write_text("unit test only", encoding="utf-8")
    Path(str(header) + ".meta").write_text("unit test only", encoding="utf-8")
    report = {
        "schema_version": 1, "reforger_version": "test", "workbench_version": "test",
        "scenario_name": "unit test, not a real game", "checks": {
            name: {"passed": True, "evidence": "synthetic test data"}
            for name in ("workbench_compile", "local_play", "listen_server", "dedicated_server", "bundle")
        }
    }
    (root / "release").mkdir()
    (root / "release" / "qa-evidence.json").write_text(json.dumps(report), encoding="utf-8")
    return world, header


class ReleaseGateTests(unittest.TestCase):
    def test_nonexistent_addon_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            errors = check_release(Path(d) / "absent")
            self.assertTrue(any("missing" in x.lower() for x in errors))

    def test_empty_addon_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            errors = check_release(Path(d))
            self.assertTrue(any("gproj" in x for x in errors))
            self.assertTrue(any(".ent" in x for x in errors))
            self.assertTrue(any(".conf" in x for x in errors))
            self.assertTrue(any("evidence" in x for x in errors))

    def test_synthetic_files_and_attestations_pass_preflight_only(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            write_fixture(root)
            self.assertEqual([], check_release(root, "local-alpha"))
            self.assertEqual([], check_release(root, "publish-candidate"))

    def test_missing_resource_metadata_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            world, header = write_fixture(root)
            Path(str(world) + ".meta").unlink()
            errors = check_release(root)
            self.assertTrue(any("Resource metadata missing" in x for x in errors))

    def test_local_not_enough_for_public_release(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            write_fixture(root)
            path = root / "release" / "qa-evidence.json"
            data = json.loads(path.read_text(encoding="utf-8"))
            data["checks"]["dedicated_server"]["passed"] = False
            path.write_text(json.dumps(data), encoding="utf-8")
            self.assertEqual([], check_release(root, "local-alpha"))
            self.assertTrue(any("dedicated_server" in x for x in check_release(root, "publish-candidate")))

    def test_no_false_pass_without_logs(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            write_fixture(root)
            path = root / "release" / "qa-evidence.json"
            data = json.loads(path.read_text(encoding="utf-8"))
            data["checks"]["workbench_compile"]["evidence"] = ""
            path.write_text(json.dumps(data), encoding="utf-8")
            self.assertTrue(any("workbench_compile" in x for x in check_release(root)))


if __name__ == "__main__":
    unittest.main()
