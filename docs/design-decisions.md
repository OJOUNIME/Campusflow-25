# Design Decisions

## Ownership
- Engineer A: ticket creation, validation, priority engine (Issues 1, 2)
- Engineer B: assignment, workflow, queue, reports (Issues 4, 5)
- JSON persistence (Issue 6): written by Engineer A, reviewed by Engineer B
- CLI menu (Issue 7): written by Engineer B, reviewed by Engineer A

## Decisions
- A ticket is a Python dict with 8 fields: id, title, category, urgency, affected_users, priority, status, assigned_to.
- Tickets are stored in a list of dicts and passed into each function as an argument.
- Invalid input raises ValueError with a clear message. The CLI catches it and prints it.
- Create, assign and status-change functions return the created or updated ticket.
- A rejected action (invalid input, unknown ID, invalid transition) leaves the ticket list unchanged.
- Only storage.py reads or writes data/tickets.json.
- Next ID = highest existing numeric ID + 1.
- Business logic has no input() or print(), so tests can call it directly.

## Stored values
- category: "Network", "Hardware", "Software", "Other"
- urgency: "low", "medium", "high" (lowercase)
- priority: "critical", "high", "medium", "low" (lowercase)
- status: "open", "in_progress", "resolved" (lowercase)
- New tickets start with status "open" and assigned_to None.

## Status rules
- open -> in_progress (only if assigned)
- in_progress -> resolved
- resolved -> open (explicit reopen only)
- Every other transition is rejected.

## Work queue
- Contains tickets with status "open" only.
- Ordered critical -> high -> medium -> low, ties broken by lower numeric ID (T2 before T10).

## Modules
- campusflow/tickets.py (A): calculate_priority, validation, create_ticket
- campusflow/workflow.py (B): assign_ticket, change_status, get_work_queue
- campusflow/reports.py (B): build_report
- campusflow/storage.py (A): load_tickets, save_tickets
- main.py (B): CLI menu