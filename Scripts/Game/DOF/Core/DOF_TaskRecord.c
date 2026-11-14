// DOF core: a task is a state machine, not an engine entity.
// Caller must have passed server-side authorization before invoking mutation.
class DOF_TaskRecord
{
    protected string m_sTaskId;
    protected DOF_ETaskState m_eState;
    protected int m_iRevision;

    void DOF_TaskRecord(string taskId)
    {
        m_sTaskId = taskId;
        m_eState = DOF_ETaskState.PLANNED;
        m_iRevision = 0;
    }

    string GetId()
    {
        return m_sTaskId;
    }

    DOF_ETaskState GetState()
    {
        return m_eState;
    }

    int GetRevision()
    {
        return m_iRevision;
    }

    bool IsTerminal()
    {
        return m_eState == DOF_ETaskState.SUCCEEDED
            || m_eState == DOF_ETaskState.FAILED
            || m_eState == DOF_ETaskState.CANCELLED;
    }

    // Revision check always precedes same-state detection:
    // outdated commands must never silently appear successful.
    DOF_ETaskResult TryTransition(DOF_ETaskState next, int expectedRevision)
    {
        if (expectedRevision != m_iRevision)
            return DOF_ETaskResult.STALE_REVISION;

        if (next == m_eState)
            return DOF_ETaskResult.SAME_STATE;

        bool allowed = false;

        switch (m_eState)
        {
            case DOF_ETaskState.PLANNED:
                allowed = next == DOF_ETaskState.AVAILABLE
                    || next == DOF_ETaskState.CANCELLED;
                break;

            case DOF_ETaskState.AVAILABLE:
                allowed = next == DOF_ETaskState.ACTIVE
                    || next == DOF_ETaskState.CANCELLED;
                break;

            case DOF_ETaskState.ACTIVE:
                allowed = next == DOF_ETaskState.PAUSED
                    || next == DOF_ETaskState.SUCCEEDED
                    || next == DOF_ETaskState.FAILED
                    || next == DOF_ETaskState.CANCELLED;
                break;

            case DOF_ETaskState.PAUSED:
                allowed = next == DOF_ETaskState.ACTIVE
                    || next == DOF_ETaskState.CANCELLED;
                break;
        }

        if (!allowed)
            return DOF_ETaskResult.ILLEGAL_TRANSITION;

        m_eState = next;
        m_iRevision++;
        return DOF_ETaskResult.APPLIED;
    }
}
