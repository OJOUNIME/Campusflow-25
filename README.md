# CampusFlow-25

## 1. Project Overview

CampusFlow is a Python command-line helpdesk application designed to help campus staff manage technical support requests. It allows users to create support tickets, calculate their priority, assign tickets to staff, track ticket status, view the work queue, generate reports, and store ticket data using JSON.

## 2. Project Objectives

- Record and manage campus technical support requests.
- Validate ticket information and reject invalid inputs.
- Calculate ticket priority using predefined business rules.
- Assign tickets to responsible staff members.
- Track ticket progress from open to resolved.
- Display unresolved tickets in priority order.
- Generate reports showing ticket totals, status, and priority.
- Save and reload tickets using JSON persistence.
- Maintain code quality through automated unit tests and GitHub code reviews.

## 3. Features

1. **Ticket Creation:** Create tickets with unique IDs and validated details.
2. **Priority Calculation:** Automatically determine ticket priority using urgency and the number of affected users.
3. **Ticket Viewing:** List tickets and view individual ticket details.
4. **Ticket Assignment:** Assign tickets to staff members.
5. **Status Management:** Track tickets through the supported workflow.
6. **Work Queue:** Display open tickets in priority order.
7. **Reports:** Summarize tickets by status and priority.
8. **JSON Persistence:** Save tickets and load them when the application restarts.
9. **Automated Testing:** Verify application behavior using Python's `unittest` framework.

## 4. Technologies Used

- Python 3
- Python standard library
- JSON for data persistence
- `unittest` for automated testing
- Git and GitHub for version control and collaboration
- Visual Studio Code for development

## 5. Project Structure

```text
Campusflow-25/
├── campusflow/
│   ├── __init__.py
│   ├── tickets.py
│   ├── workflow.py
│   ├── storage.py
│   └── reports.py
├── tests/
│   ├── __init__.py
│   ├── test_tickets.py
│   ├── test_workflow.py
│   └── test_storage.py
├── docs/
│   ├── design-decisions.md
│   └── ai-learning-log.md
├── data/
│   └── tickets.json
├── main.py
├── README.md
└── .gitignore
```

*Note: The `data/tickets.json` file is generated at runtime and should not be committed to Git. Some files or folders may be absent until their features are implemented.*

## 6. Requirements

- Python 3.12 or a compatible Python 3 version.
- Git.
- A terminal or command-line interface.

No third-party Python packages are required.

## 7. How to Run the Project

### Step 1: Clone the repository

```bash
git clone <Repository: https://github.com/OJOUNIME/Campusflow-25>
cd Campusflow-25
```

Replace the placeholder with your team's actual GitHub repository URL.

### Step 2: Run the application

```bash
python3 main.py
```

The command-line menu will allow users to interact with the available features.

### Step 3: Run the automated tests

```bash
python3 -m unittest discover -s tests -p "test_*.py" -v
```

This command discovers and runs the project's automated tests.

## 8. Ticket Data Structure

Each ticket is represented as a Python dictionary containing the following fields:

| Field | Description |
|---|---|
| `id` | Unique ticket identifier, such as `T001` |
| `title` | Description of the reported problem |
| `category` | Network, Hardware, Software, or Other |
| `urgency` | low, medium, or high |
| `affected_users` | Positive integer representing affected users |
| `priority` | critical, high, medium, or low |
| `status` | open, in_progress, or resolved |
| `assigned_to` | Staff member's name or `None` |

## 9. Priority Rules

Priority is calculated using the following rules in order:

1. High urgency and at least 10 affected users: `critical`.
2. High urgency or at least 10 affected users: `high`.
3. Medium urgency or at least 3 affected users: `medium`.
4. All remaining valid tickets: `low`.

These rules are ordinary Python business logic, not an AI-based priority model.

## 10. Team Responsibilities

### Engineer A — Ticket Management and Persistence

- Ticket creation and input validation.
- Priority calculation.
- Automated tests for ticket creation and priority calculation.
- JSON storage and retrieval.
- Review of Engineer B's pull request.

### Engineer B — Workflow and Reporting

- Ticket assignment.
- Status changes and workflow validation.
- Work queue management.
- Reports and summaries.
- Automated tests for workflow and reporting.
- Review of Engineer A's pull request.

Both engineers contribute code and tests, review each other's pull requests, and participate in integration and demonstration.

## 11. Collaboration and Version Control

The team uses Git and GitHub to collaborate.

- Each engineer works on a separate feature branch.
- Changes are committed and pushed to GitHub.
- Each engineer opens a pull request for their work.
- The other engineer reviews the code and provides substantive feedback.
- Changes are approved and merged into `main` only after the required review and checks.
- The team runs the complete test suite after integration.

## 12. Testing

Automated tests use Python's built-in `unittest` framework. Tests cover priority calculation, ticket creation, input validation, workflow rules, and JSON persistence as the corresponding features are implemented.

Run all tests using:

```bash
python3 -m unittest discover -s tests -p "test_*.py" -v
```

## 13. AI-Assisted Learning

AI tools are used to explain programming concepts, explore edge cases, investigate errors, and critique implementation decisions. Suggestions are independently tested and evaluated before being adopted.

The team's learning records are maintained in `docs/ai-learning-log.md`.

## 14. Project Status

CampusFlow-25 is being developed collaboratively. Features, tests, documentation, and integration checks should be marked complete only after they have been implemented and verified.

## 15. Team Members

- Engineer A: [Elijah Mamodu]
- Engineer B: [Okefu Enyitobi]
