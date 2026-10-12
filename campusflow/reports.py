"""Ticket summary report (Okefu Enyitobi)."""

from campusflow.workflow import ALLOWED_TRANSITIONS, PRIORITY_RANK


def build_report(tickets):
    """Return counts of tickets overall, by status and by priority.

    Shape: {"total": int, "by_status": {...}, "by_priority": {...}}
    Every valid status and priority is always present, even when its count is 0.
    Raises ValueError if a ticket has an unknown status or priority.
    Does not modify the tickets list.
    """
        # Start every count at 0 using the keys of the two workflow dicts, so all
    # valid statuses and priorities show up even when no ticket uses them.
    # Python dicts keep insertion order, so the report lists them in the same
    # order as workflow.py: open -> in_progress -> resolved, critical -> low.
    by_status = {status: 0 for status in ALLOWED_TRANSITIONS}
    by_priority = {priority: 0 for priority in PRIORITY_RANK}

    for ticket in tickets:
        status = ticket["status"]
        priority = ticket["priority"]
        if status not in by_status:
            raise ValueError(f"Unknown status in ticket {ticket['id']}: {status}")
        if priority not in by_priority:
            raise ValueError(f"Unknown priority in ticket {ticket['id']}: {priority}")
        by_status[status] += 1
        by_priority[priority] += 1

    return {
        "total": len(tickets),
        "by_status": by_status,
        "by_priority": by_priority,
    }