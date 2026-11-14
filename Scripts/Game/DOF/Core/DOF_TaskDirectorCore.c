// Pure mission state machine. Contains NO RPC, spawning or UI hooks.
// It must only be owned/called by a future authoritative server-side adapter.
// Registrations require predecessor tasks to exist (topological order).
class DOF_TaskEntry
{
    protected ref DOF_TaskRecord m_Task;
    protected ref array<string> m_aPredecessors = {};

    void DOF_TaskEntry(DOF_TaskRecord task, array<string> predecessors)
    {
        m_Task = task;

        if (!predecessors)
            return;

        foreach (string predecessor : predecessors)
        {
            m_aPredecessors.Insert(predecessor);
        }
    }

    DOF_TaskRecord GetTask()
    {
        return m_Task;
    }

    int GetPredecessorCount()
    {
        return m_aPredecessors.Count();
    }

    string GetPredecessor(int index)
    {
        return m_aPredecessors[index];
    }
}

class DOF_TaskDirectorCore
{
    protected ref array<ref DOF_TaskEntry> m_aEntries = {};
    protected bool m_bStarted;

    protected DOF_TaskEntry FindEntry(string taskId)
    {
        foreach (DOF_TaskEntry entry : m_aEntries)
        {
            if (entry.GetTask().GetId() == taskId)
                return entry;
        }

        return null;
    }

    // A new task may depend only on already registered tasks.
    // This makes dependency cycles impossible by construction.
    bool AddTask(string taskId, array<string> predecessors)
    {
        if (taskId == "" || FindEntry(taskId))
            return false;

        if (m_aEntries.Count() >= 64)
            return false;

        ref array<string> validPredecessors = {};

        if (predecessors)
        {
            if (predecessors.Count() > 16)
                return false;

            foreach (string predecessor : predecessors)
            {
                if (predecessor == "" || predecessor == taskId)
                    return false;

                if (!FindEntry(predecessor))
                    return false;

                foreach (string previous : validPredecessors)
                {
                    if (previous == predecessor)
                        return false;
                }

                validPredecessors.Insert(predecessor);
            }
        }

        DOF_TaskRecord task = new DOF_TaskRecord(taskId);
        DOF_TaskEntry entry = new DOF_TaskEntry(task, validPredecessors);
        m_aEntries.Insert(entry);

        // A task added during an operation can become available
        // immediately if all predecessors already succeeded.
        if (m_bStarted)
            RefreshAvailability();

        return true;
    }

    bool StartMission()
    {
        if (m_bStarted)
            return false;

        m_bStarted = true;
        RefreshAvailability();
        return true;
    }

    int GetTaskCount()
    {
        return m_aEntries.Count();
    }

    // Read-only snapshot surface: callers cannot change tasks through it.
    bool ReadTask(string taskId, out DOF_ETaskState state, out int revision)
    {
        DOF_TaskEntry entry = FindEntry(taskId);

        if (!entry)
            return false;

        state = entry.GetTask().GetState();
        revision = entry.GetTask().GetRevision();
        return true;
    }

    // NEVER call directly from an untrusted client request.
    // The later RPC adapter must verify identity, role and permissions.
    DOF_ETaskResult RequestState(string taskId, DOF_ETaskState next, int expectedRevision)
    {
        if (!m_bStarted)
            return DOF_ETaskResult.NOT_STARTED;

        DOF_TaskEntry entry = FindEntry(taskId);

        if (!entry)
            return DOF_ETaskResult.NOT_FOUND;

        DOF_TaskRecord task = entry.GetTask();

        // Check the revision first, including for blocked unlock attempts.
        if (expectedRevision != task.GetRevision())
            return DOF_ETaskResult.STALE_REVISION;

        if (next == DOF_ETaskState.AVAILABLE && !DependenciesSatisfied(entry))
            return DOF_ETaskResult.PREREQUISITES_PENDING;

        DOF_ETaskResult result = task.TryTransition(next, expectedRevision);

        if (result == DOF_ETaskResult.APPLIED && next == DOF_ETaskState.SUCCEEDED)
            RefreshAvailability();

        return result;
    }

    protected bool DependenciesSatisfied(DOF_TaskEntry entry)
    {
        for (int i = 0; i < entry.GetPredecessorCount(); i++)
        {
            DOF_TaskEntry predecessor = FindEntry(entry.GetPredecessor(i));

            if (!predecessor)
                return false;

            if (predecessor.GetTask().GetState() != DOF_ETaskState.SUCCEEDED)
                return false;
        }

        return true;
    }

    protected void RefreshAvailability()
    {
        foreach (DOF_TaskEntry entry : m_aEntries)
        {
            DOF_TaskRecord task = entry.GetTask();

            if (task.GetState() != DOF_ETaskState.PLANNED)
                continue;

            if (!DependenciesSatisfied(entry))
                continue;

            task.TryTransition(DOF_ETaskState.AVAILABLE, task.GetRevision());
        }
    }
}
