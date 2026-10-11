
def calculate_priority(urgency, affected_users):
    """Calculates ticket priority based on urgency and number of affected users."""
    if urgency == "high":
        if affected_users >= 10:
            return "critical"
        return "high"
    else:  # urgency == "low" or "medium"
        if affected_users >= 10:
            return "high"
        elif affected_users >= 3:
            return "medium"
        return "low"


def create_ticket(tickets, title, category, urgency, affected_users):
    """Create a new ticket dict, append it to tickets, and return it."""
    # 1. Deduce the next numerical ID
    existing_ids = [t["id"] for t in tickets if "id" in t]
    
    numeric_ids = []
    for ticket_id in existing_ids:
        if ticket_id.startswith("T"):
            try:
                numeric_ids.append(int(ticket_id[1:]))
            except ValueError:
                pass
                
    highest_id = max(numeric_ids) if numeric_ids else 0
    next_id = f"T{highest_id + 1:03d}"

    # 2. Build the ticket dictionary object
    new_ticket = {
        "id": next_id,
        "title": title,
        "category": category,
        "urgency": urgency,
        "affected_users": affected_users,
        # Call with the correct 2 parameters expected by the system tests
        "priority": calculate_priority(urgency, affected_users),
        "status": "open",
        "assigned_to": None
    }

    # 3. Append to system array tracking list and return the dict
    tickets.append(new_ticket)
    return new_ticket
