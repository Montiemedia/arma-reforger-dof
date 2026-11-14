// DOF core: engine-independent value types.
// Candidate for Enforce Workbench compilation; not yet compiled in target version.
[EnumLinear()]
enum DOF_ETaskState
{
    PLANNED,
    AVAILABLE,
    ACTIVE,
    PAUSED,
    SUCCEEDED,
    FAILED,
    CANCELLED
}

[EnumLinear()]
enum DOF_ETaskResult
{
    APPLIED,
    SAME_STATE,
    STALE_REVISION,
    ILLEGAL_TRANSITION,
    NOT_FOUND,
    PREREQUISITES_PENDING,
    NOT_STARTED
}
