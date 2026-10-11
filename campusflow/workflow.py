"""Assignment, status workflow and work queue (Engineer B)."""

VALID_STATUSES = {"open", "in_progress", "resolved"}

ALLOWED_TRANSITIONS = {
    "open": ["in_progress"],
    "in_progress": ["resolved"],
    "resolved": ["open"],  # reopen
}

PRIORITY_RANK = {"critical": 0, "high": 1, "medium": 2, "low": 3}


def _find_ticket(tickets, ticket_id):
    """Return the ticket dict with this id, or raise ValueError if not found."""
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            return ticket
    raise ValueError(f"Ticket {ticket_id} not found")


def assign_ticket(tickets, ticket_id, name):
    """Assign a ticket to a staff member.

    Raises ValueError for an unknown ticket id or a blank name.
    Returns the updated ticket.
    """
    ticket = _find_ticket(tickets, ticket_id)
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Assignee name cannot be blank")
    ticket["assigned_to"] = name.strip()
    return ticket


def change_status(tickets, ticket_id, new_status):
    """Move a ticket to new_status if the transition is allowed.

    Rules: open -> in_progress (only if assigned), in_progress -> resolved,
    resolved -> open (reopen). Everything else raises ValueError.
    A rejected change must leave the ticket unchanged.
    Returns the updated ticket.
    """
    ticket = _find_ticket(tickets, ticket_id)

    if new_status not in VALID_STATUSES:
        raise ValueError(f"Unknown status: {new_status}")

    current = ticket["status"]
    if new_status not in ALLOWED_TRANSITIONS.get(current, []):
        raise ValueError(f"Cannot move from {current} to {new_status}")

    if new_status == "in_progress" and not ticket.get("assigned_to"):
        raise ValueError("Ticket must be assigned before it can be in progress")

    ticket["status"] = new_status  # only change the ticket after every check passed
    return ticket


def get_work_queue(tickets):
    """Return open tickets sorted critical -> high -> medium -> low,
    ties broken by lower numeric id (T2 before T10).
    Must not modify the original list.
    """
    open_tickets = [t for t in tickets if t["status"] == "open"]
    return sorted(
        open_tickets,
        key=lambda t: (PRIORITY_RANK[t["priority"]], int(t["id"][1:])),
    )