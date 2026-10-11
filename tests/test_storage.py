import unittest
import os
from campusflow.storage import load_tickets, save_tickets
from campusflow.tickets import create_ticket

class TestStoragePersistence(unittest.TestCase):
    def setUp(self):
        self.test_file = "tests/test_tickets_tmp.json"
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_missing_file_returns_empty_list(self):
        tickets = load_tickets(self.test_file)
        self.assertEqual(tickets, [])

    def test_save_and_reload_preserves_tickets(self):
        tickets_list = []
        create_ticket(tickets_list, "Server Down", "Network", "high", 15)
        save_tickets(tickets_list, self.test_file)
        reloaded_tickets = load_tickets(self.test_file)
        self.assertEqual(len(reloaded_tickets), 1)
        self.assertEqual(reloaded_tickets[0]["title"], "Server Down")
        self.assertEqual(reloaded_tickets[0]["priority"], "critical")

    def test_create_after_reload_gives_no_duplicate_id(self):
        tickets_list = [{"id": "T005", "title": "Old Ticket", "category": "Other", "urgency": "low", "affected_users": 1, "priority": "low", "status": "open", "assigned_to": None}]
        save_tickets(tickets_list, self.test_file)
        fresh_tickets_list = load_tickets(self.test_file)
        new_ticket = create_ticket(fresh_tickets_list, "New Issue", "Software", "medium", 2)
        self.assertEqual(new_ticket["id"], "T006")

    def test_corrupted_json_handled(self):
        os.makedirs(os.path.dirname(self.test_file), exist_ok=True)
        with open(self.test_file, "w") as f:
            f.write("{ invalid json data ... [")
        with self.assertRaises(ValueError):
            load_tickets(self.test_file)

if __name__ == "__main__":
    unittest.main()
