import unittest
from campusflow.workflow import assign_ticket, change_status, get_work_queue


def make_ticket(ticket_id="T001", priority="low", status="open", assigned_to=None):
    return {
        "id": ticket_id, "title": "Test", "category": "Other",
        "urgency": "low", "affected_users": 1,
        "priority": priority, "status": status, "assigned_to": assigned_to,
    }


class TestAssign(unittest.TestCase):
    def test_assign_valid(self):
        tickets = [make_ticket("T001")]
        result = assign_ticket(tickets, "T001", "Sam")
        self.assertEqual(result["assigned_to"], "Sam")
        self.assertEqual(tickets[0]["assigned_to"], "Sam")

    def test_assign_trims_whitespace(self):
        tickets = [make_ticket("T001")]
        assign_ticket(tickets, "T001", "  Sam  ")
        self.assertEqual(tickets[0]["assigned_to"], "Sam")

    def test_assign_unknown_id_rejected(self):
        tickets = [make_ticket("T001")]
        with self.assertRaises(ValueError):
            assign_ticket(tickets, "T999", "Sam")
        self.assertIsNone(tickets[0]["assigned_to"])

    def test_assign_blank_name_rejected(self):
        tickets = [make_ticket("T001")]
        for bad_name in ["", "   ", None]:
            with self.subTest(name=bad_name):
                with self.assertRaises(ValueError):
                    assign_ticket(tickets, "T001", bad_name)
                self.assertIsNone(tickets[0]["assigned_to"])


class TestStatus(unittest.TestCase):
    def test_unassigned_cannot_start(self):
        tickets = [make_ticket("T001")]
        with self.assertRaises(ValueError):
            change_status(tickets, "T001", "in_progress")
        self.assertEqual(tickets[0]["status"], "open")

    def test_full_lifecycle(self):
        tickets = [make_ticket("T001")]
        assign_ticket(tickets, "T001", "Sam")
        change_status(tickets, "T001", "in_progress")
        self.assertEqual(tickets[0]["status"], "in_progress")
        change_status(tickets, "T001", "resolved")
        self.assertEqual(tickets[0]["status"], "resolved")

    def test_invalid_transition_rejected(self):
        tickets = [make_ticket("T001", assigned_to="Sam")]
        with self.assertRaises(ValueError):
            change_status(tickets, "T001", "resolved")   # open -> resolved
        self.assertEqual(tickets[0]["status"], "open")

    def test_unknown_status_rejected(self):
        tickets = [make_ticket("T001", assigned_to="Sam")]
        with self.assertRaises(ValueError):
            change_status(tickets, "T001", "done")
        self.assertEqual(tickets[0]["status"], "open")

    def test_reopen_resolved(self):
        tickets = [make_ticket("T001", status="resolved", assigned_to="Sam")]
        change_status(tickets, "T001", "open")
        self.assertEqual(tickets[0]["status"], "open")

    def test_rejected_change_leaves_ticket_unchanged(self):
        ticket = make_ticket("T001", assigned_to="Sam")
        tickets = [ticket]
        before = dict(ticket)
        with self.assertRaises(ValueError):
            change_status(tickets, "T001", "resolved")
        self.assertEqual(ticket, before)


class TestQueue(unittest.TestCase):
    def test_priority_order(self):
        tickets = [
            make_ticket("T1", priority="low"),
            make_ticket("T2", priority="critical"),
            make_ticket("T3", priority="medium"),
            make_ticket("T4", priority="high"),
        ]
        ids = [t["id"] for t in get_work_queue(tickets)]
        self.assertEqual(ids, ["T2", "T4", "T3", "T1"])

    def test_tie_broken_by_numeric_id(self):
        tickets = [
            make_ticket("T10", priority="high"),
            make_ticket("T2", priority="high"),
        ]
        ids = [t["id"] for t in get_work_queue(tickets)]
        self.assertEqual(ids, ["T2", "T10"])

    def test_only_open_tickets_in_queue(self):
        tickets = [
            make_ticket("T1"),
            make_ticket("T2", status="in_progress", assigned_to="Sam"),
            make_ticket("T3", status="resolved", assigned_to="Sam"),
        ]
        ids = [t["id"] for t in get_work_queue(tickets)]
        self.assertEqual(ids, ["T1"])

    def test_original_list_not_modified(self):
        tickets = [
            make_ticket("T3", priority="low"),
            make_ticket("T1", priority="critical"),
            make_ticket("T2", priority="high"),
        ]
        order_before = [t["id"] for t in tickets]
        get_work_queue(tickets)
        self.assertEqual([t["id"] for t in tickets], order_before)

    def test_empty_queue(self):
        self.assertEqual(get_work_queue([]), [])


if __name__ == "__main__":
    unittest.main()