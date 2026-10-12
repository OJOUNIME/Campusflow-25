
import json
from pathlib import Path

from campusflow.tickets import create_ticket
from campusflow.workflow import assign_ticket, change_status, get_work_queue
from campusflow.reports import build_report
from campusflow.storage import load_tickets, save_tickets


DATA_DIR = Path("data")
DATA_FILE = DATA_DIR / "tickets.json"


def display_ticket(ticket):
    """Display the details of one ticket."""
    print("\n--- Ticket Details ---")
    for field, value in ticket.items():
        print(f"{field}: {value}")


def find_ticket(tickets, ticket_id):
    """Find a ticket by its ID."""
    for ticket in tickets:
        if ticket["id"].upper() == ticket_id.strip().upper():
            return ticket
    return None


def main():
    """Run the CampusFlow command-line application."""
    DATA_DIR.mkdir(exist_ok=True)

    try:
        tickets = load_tickets(str(DATA_FILE))
    except (json.JSONDecodeError, OSError, ValueError) as error:
        print(f"Could not load saved tickets: {error}")
        print("Please check the JSON file before continuing.")
        return

    if tickets is None:
        tickets = []

    while True:
        print("\n===== CAMPUSFLOW HELPDESK =====")
        print("1. Create ticket")
        print("2. List all tickets")
        print("3. View one ticket")
        print("4. Assign ticket")
        print("5. Change ticket status")
        print("6. View work queue")
        print("7. View reports")
        print("8. Save tickets")
        print("9. Exit")

        choice = input("Choose an option (1-9): ").strip()

        try:
            if choice == "1":
                title = input("Ticket title: ")
                category = input(
                    "Category (Network/Hardware/Software/Other): "
                )
                urgency = input("Urgency (low/medium/high): ")
                affected_users = int(input("Number of affected users: "))

                ticket = create_ticket(
                    tickets,
                    title,
                    category,
                    urgency,
                    affected_users
                )

                save_tickets(tickets, str(DATA_FILE))
                print("\nTicket created successfully!")
                display_ticket(ticket)

            elif choice == "2":
                if not tickets:
                    print("No tickets found.")
                else:
                    for ticket in tickets:
                        display_ticket(ticket)

            elif choice == "3":
                ticket_id = input("Enter ticket ID: ")
                ticket = find_ticket(tickets, ticket_id)

                if ticket is None:
                    print("Error: Ticket not found.")
                else:
                    display_ticket(ticket)

            elif choice == "4":
                ticket_id = input("Enter ticket ID: ")
                staff_name = input("Enter staff member's name: ").strip()

                if find_ticket(tickets, ticket_id) is None:
                    print("Error: Ticket not found.")
                elif not staff_name:
                    print("Error: Staff name cannot be empty.")
                else:
                    assign_ticket(tickets, ticket_id, staff_name)
                    save_tickets(tickets, str(DATA_FILE))
                    print("Ticket assigned successfully.")

            elif choice == "5":
                ticket_id = input("Enter ticket ID: ")
                new_status = input(
                    "New status (open/in_progress/resolved): "
                ).strip().lower()

                if find_ticket(tickets, ticket_id) is None:
                    print("Error: Ticket not found.")
                else:
                    change_status(tickets, ticket_id, new_status)
                    save_tickets(tickets, str(DATA_FILE))
                    print("Ticket status updated successfully.")

            elif choice == "6":
                queue = get_work_queue(tickets)

                if not queue:
                    print("There are no open tickets.")
                else:
                    print("\n--- Work Queue ---")
                    for ticket in queue:
                        display_ticket(ticket)

            elif choice == "7":
                report = build_report(tickets)
                print("\n--- Ticket Reports ---")
                print(report)

            elif choice == "8":
                save_tickets(tickets, str(DATA_FILE))
                print("Tickets saved successfully.")

            elif choice == "9":
                save_tickets(tickets, str(DATA_FILE))
                print("Tickets saved. Goodbye!")
                break

            else:
                print("Invalid option. Choose a number from 1 to 9.")

        except (ValueError, TypeError, KeyError) as error:
            print(f"Error: {error}")

        except OSError as error:
            print(f"File operation failed: {error}")


if __name__ == "__main__":
    main()
 