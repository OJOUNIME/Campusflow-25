"""Ticket summary report (Okefu Enyitobi)."""

from campusflow.workflow import ALLOWED_TRANSITIONS, PRIORITY_RANK


def build_report(tickets):
    """Return counts of tickets overall, by status and by priority.

    Shape: {"total": int, "by_status": {...}, "by_priority": {...}}
    Every valid status and priority is always present, even when its count is 0.
    Raises ValueError if a ticket has a missing, non-string or unknown status
    or priority.
    Does not modify the tickets list.
    """
    # Start every count at 0 using the keys of the two workflow dicts, so all
    # valid statuses and priorities show up even when no ticket uses them.
    # Dicts keep insertion order, so the report follows workflow.py's order.
    by_status = {status: 0 for status in ALLOWED_TRANSITIONS}
    by_priority = {priority: 0 for priority in PRIORITY_RANK}

    for ticket in tickets:
        ticket_id = ticket.get("id", "<no id>")
        status = ticket.get("status")
        priority = ticket.get("priority")

        if not isinstance(status, str) or status not in by_status:
            raise ValueError(f"Unknown status in ticket {ticket_id}: {status!r}")
        if not isinstance(priority, str) or priority not in by_priority:
            raise ValueError(f"Unknown priority in ticket {ticket_id}: {priority!r}")

        by_status[status] += 1
        by_priority[priority] += 1

    return {
        "total": len(tickets),
        "by_status": by_status,
        "by_priority": by_priority,
    }