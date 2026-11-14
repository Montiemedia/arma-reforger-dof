"""Test the Python reference behavior, NOT compiled Enforce Script."""

import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from dof_task_reference import TaskDirectorCore, TaskResult, TaskState


def mission():
    director = TaskDirectorCore()
    assert director.add_task("approach")
    assert director.add_task("clear", ["approach"])
    assert director.add_task("defend", ["clear"])
    assert director.start_mission()
    return director


class TaskDirectorReferenceTests(unittest.TestCase):
    def test_initial_availability_and_single_start(self):
        director = mission()
        self.assertEqual((TaskState.AVAILABLE, 1), director.snapshot("approach"))
        self.assertEqual((TaskState.PLANNED, 0), director.snapshot("clear"))
        self.assertEqual((TaskState.PLANNED, 0), director.snapshot("defend"))
        self.assertFalse(director.start_mission())

    def test_three_stage_success_path(self):
        director = mission()
        for name in ("approach", "clear", "defend"):
            state, rev = director.snapshot(name)
            self.assertEqual(TaskState.AVAILABLE, state)
            self.assertEqual(
                TaskResult.APPLIED,
                director.request_state(name, TaskState.ACTIVE, rev),
            )
            self.assertEqual(
                TaskResult.APPLIED,
                director.request_state(name, TaskState.SUCCEEDED, rev + 1),
            )
        self.assertEqual((TaskState.SUCCEEDED, 3), director.snapshot("defend"))

    def test_stale_revision_and_duplicate_state(self):
        director = mission()
        self.assertEqual(
            TaskResult.APPLIED,
            director.request_state("approach", TaskState.ACTIVE, 1),
        )
        self.assertEqual(
            TaskResult.STALE_REVISION,
            director.request_state("approach", TaskState.ACTIVE, 1),
        )
        self.assertEqual(
            TaskResult.SAME_STATE,
            director.request_state("approach", TaskState.ACTIVE, 2),
        )
        self.assertEqual((TaskState.ACTIVE, 2), director.snapshot("approach"))

    def test_blocked_follow_up_cannot_start(self):
        director = mission()
        self.assertEqual(
            TaskResult.PREREQUISITES_PENDING,
            director.request_state("clear", TaskState.AVAILABLE, 0),
        )
        self.assertEqual(
            TaskResult.ILLEGAL_TRANSITION,
            director.request_state("clear", TaskState.ACTIVE, 0),
        )

    def test_failure_does_not_unlock_next_task(self):
        director = mission()
        director.request_state("approach", TaskState.ACTIVE, 1)
        director.request_state("approach", TaskState.FAILED, 2)
        self.assertEqual((TaskState.PLANNED, 0), director.snapshot("clear"))
        self.assertEqual(
            TaskResult.ILLEGAL_TRANSITION,
            director.request_state("approach", TaskState.ACTIVE, 3),
        )

    def test_cancelled_task_is_terminal(self):
        director = mission()
        self.assertEqual(
            TaskResult.APPLIED,
            director.request_state("approach", TaskState.CANCELLED, 1),
        )
        self.assertEqual(
            TaskResult.ILLEGAL_TRANSITION,
            director.request_state("approach", TaskState.AVAILABLE, 2),
        )
        self.assertEqual((TaskState.PLANNED, 0), director.snapshot("clear"))

    def test_pausing_and_resuming(self):
        director = mission()
        director.request_state("approach", TaskState.ACTIVE, 1)
        self.assertEqual(
            TaskResult.APPLIED,
            director.request_state("approach", TaskState.PAUSED, 2),
        )
        self.assertEqual(
            TaskResult.APPLIED,
            director.request_state("approach", TaskState.ACTIVE, 3),
        )

    def test_dynamic_task_added_after_predecessor_success(self):
        director = TaskDirectorCore()
        self.assertTrue(director.add_task("first"))
        director.start_mission()
        director.request_state("first", TaskState.ACTIVE, 1)
        director.request_state("first", TaskState.SUCCEEDED, 2)
        self.assertTrue(director.add_task("late", ["first"]))
        self.assertEqual((TaskState.AVAILABLE, 1), director.snapshot("late"))

    def test_duplicate_missing_and_self_dependencies_rejected(self):
        director = TaskDirectorCore()
        self.assertFalse(director.add_task("bad", ["missing"]))
        self.assertFalse(director.add_task("bad", ["bad"]))
        self.assertTrue(director.add_task("first"))
        self.assertFalse(director.add_task("first"))
        self.assertFalse(director.add_task("second", ["first", "first"]))
        self.assertTrue(director.add_task("second", ["first"]))

    def test_invalid_before_start_and_unknown(self):
        director = TaskDirectorCore()
        self.assertTrue(director.add_task("first"))
        self.assertEqual(
            TaskResult.NOT_STARTED,
            director.request_state("first", TaskState.ACTIVE, 0),
        )
        director.start_mission()
        self.assertEqual(
            TaskResult.NOT_FOUND,
            director.request_state("missing", TaskState.ACTIVE, 0),
        )
        self.assertIsNone(director.snapshot("missing"))

    def test_multiple_dependencies(self):
        director = TaskDirectorCore()
        self.assertTrue(director.add_task("alpha"))
        self.assertTrue(director.add_task("bravo"))
        self.assertTrue(director.add_task("combined", ["alpha", "bravo"]))
        director.start_mission()
        director.request_state("alpha", TaskState.ACTIVE, 1)
        director.request_state("alpha", TaskState.SUCCEEDED, 2)
        self.assertEqual((TaskState.PLANNED, 0), director.snapshot("combined"))
        director.request_state("bravo", TaskState.ACTIVE, 1)
        director.request_state("bravo", TaskState.SUCCEEDED, 2)
        self.assertEqual((TaskState.AVAILABLE, 1), director.snapshot("combined"))

    def test_maximum_tasks_guard(self):
        director = TaskDirectorCore()
        for i in range(64):
            self.assertTrue(director.add_task(f"task_{i}"))
        self.assertFalse(director.add_task("task_64"))


if __name__ == "__main__":
    unittest.main()
