"""Executable *reference* specification of DOF task transitions.

This is Python, NOT an Enforce runtime or compiler. Its policy is intended to
match Scripts/Game/DOF/Core, which still requires Workbench compilation.
"""

from dataclasses import dataclass
from enum import IntEnum


class TaskState(IntEnum):
    PLANNED = 0
    AVAILABLE = 1
    ACTIVE = 2
    PAUSED = 3
    SUCCEEDED = 4
    FAILED = 5
    CANCELLED = 6


class TaskResult(IntEnum):
    APPLIED = 0
    SAME_STATE = 1
    STALE_REVISION = 2
    ILLEGAL_TRANSITION = 3
    NOT_FOUND = 4
    PREREQUISITES_PENDING = 5
    NOT_STARTED = 6


ALLOWED = {
    TaskState.PLANNED: {TaskState.AVAILABLE, TaskState.CANCELLED},
    TaskState.AVAILABLE: {TaskState.ACTIVE, TaskState.CANCELLED},
    TaskState.ACTIVE: {
        TaskState.PAUSED, TaskState.SUCCEEDED, TaskState.FAILED,
        TaskState.CANCELLED,
    },
    TaskState.PAUSED: {TaskState.ACTIVE, TaskState.CANCELLED},
    TaskState.SUCCEEDED: set(),
    TaskState.FAILED: set(),
    TaskState.CANCELLED: set(),
}


@dataclass
class TaskRecord:
    task_id: str
    state: TaskState = TaskState.PLANNED
    revision: int = 0

    def transition(self, next_state: TaskState, expected_revision: int) -> TaskResult:
        if expected_revision != self.revision:
            return TaskResult.STALE_REVISION
        if next_state == self.state:
            return TaskResult.SAME_STATE
        if next_state not in ALLOWED[self.state]:
            return TaskResult.ILLEGAL_TRANSITION
        self.state = next_state
        self.revision += 1
        return TaskResult.APPLIED


class TaskDirectorCore:
    """Trusted single-authority model. Not a server authentication boundary."""

    def __init__(self):
        self._tasks: dict[str, TaskRecord] = {}
        self._requires: dict[str, tuple[str, ...]] = {}
        self._started = False

    def add_task(self, task_id: str, predecessors=()) -> bool:
        if not isinstance(task_id, str) or not task_id or task_id in self._tasks:
            return False
        if len(self._tasks) >= 64:
            return False
        if not isinstance(predecessors, (tuple, list)) or len(predecessors) > 16:
            return False
        if any(
            not isinstance(p, str) or not p or p == task_id or p not in self._tasks
            for p in predecessors
        ):
            return False
        if len(set(predecessors)) != len(predecessors):
            return False

        self._tasks[task_id] = TaskRecord(task_id)
        self._requires[task_id] = tuple(predecessors)
        if self._started:
            self._refresh_availability()
        return True

    def start_mission(self) -> bool:
        if self._started:
            return False
        self._started = True
        self._refresh_availability()
        return True

    def snapshot(self, task_id: str) -> tuple[TaskState, int] | None:
        task = self._tasks.get(task_id)
        if task is None:
            return None
        return task.state, task.revision

    def request_state(
        self, task_id: str, next_state: TaskState, expected_revision: int
    ) -> TaskResult:
        if not self._started:
            return TaskResult.NOT_STARTED
        task = self._tasks.get(task_id)
        if task is None:
            return TaskResult.NOT_FOUND
        if expected_revision != task.revision:
            return TaskResult.STALE_REVISION
        if next_state == TaskState.AVAILABLE and not self._dependencies_satisfied(task_id):
            return TaskResult.PREREQUISITES_PENDING

        result = task.transition(next_state, expected_revision)
        if result == TaskResult.APPLIED and next_state == TaskState.SUCCEEDED:
            self._refresh_availability()
        return result

    def _dependencies_satisfied(self, task_id: str) -> bool:
        return all(
            self._tasks[predecessor].state == TaskState.SUCCEEDED
            for predecessor in self._requires[task_id]
        )

    def _refresh_availability(self) -> None:
        for task_id, task in self._tasks.items():
            if task.state == TaskState.PLANNED and self._dependencies_satisfied(task_id):
                task.transition(TaskState.AVAILABLE, task.revision)
