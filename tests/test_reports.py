import copy
import unittest

from campusflow.reports import build_report
from campusflow.tickets import create_ticket


def make_ticket(ticket_id, status="open", priority="medium", assigned_to=None):
    return {
        "id": ticket_id,
        "status": status,
        "priority": priority,
        "assigned_to": assigned_to,
    }


class BuildReportTests(unittest.TestCase):
    def test_empty_list_has_full_shape_with_zeros(self):
        report = build_report([])
        self.assertEqual(report["total"], 0)
        self.assertEqual(
            report["by_status"], {"open": 0, "in_progress": 0, "resolved": 0}
        )
        self.assertEqual(
            report["by_priority"],
            {"critical": 0, "high": 0, "medium": 0, "low": 0},
        )

    def test_counts_by_status_and_priority(self):
        tickets = [
            make_ticket("T001", "open", "critical"),
            make_ticket("T002", "open", "low"),
            make_ticket("T003", "in_progress", "high", "Ana"),
            make_ticket("T004", "resolved", "high", "Ben"),
        ]
        report = build_report(tickets)
        self.assertEqual(report["total"], 4)
        self.assertEqual(
            report["by_status"], {"open": 2, "in_progress": 1, "resolved": 1}
        )
        self.assertEqual(
            report["by_priority"],
            {"critical": 1, "high": 2, "medium": 0, "low": 1},
        )

    def test_missing_categories_still_appear_as_zero(self):
        report = build_report([make_ticket("T001", "open", "low")])
        self.assertEqual(report["by_status"]["resolved"], 0)
        self.assertEqual(report["by_priority"]["critical"], 0)

    def test_keys_are_in_workflow_order(self):
        # assertEqual on dicts ignores key order, so compare the key lists.
        report = build_report([])
        self.assertEqual(
            list(report["by_status"]), ["open", "in_progress", "resolved"]
        )
        self.assertEqual(
            list(report["by_priority"]), ["critical", "high", "medium", "low"]
        )

    def test_totals_match_sums(self):
        tickets = [
            make_ticket("T001", "open", "critical"),
            make_ticket("T002", "resolved", "medium"),
            make_ticket("T003", "in_progress", "low", "Ana"),
        ]
        report = build_report(tickets)
        self.assertEqual(sum(report["by_status"].values()), report["total"])
        self.assertEqual(sum(report["by_priority"].values()), report["total"])

    def test_unknown_status_raises(self):
        with self.assertRaises(ValueError):
            build_report([make_ticket("T001", "banana", "low")])

    def test_unknown_priority_raises(self):
        with self.assertRaises(ValueError):
            build_report([make_ticket("T001", "open", "urgent")])

    def test_does_not_modify_input(self):
        tickets = [
            make_ticket("T001", "open", "high"),
            make_ticket("T002", "resolved", "low"),
        ]
        snapshot = copy.deepcopy(tickets)
        build_report(tickets)
        self.assertEqual(tickets, snapshot)

    # ---- Added after review ----

    def test_missing_status_raises_value_error(self):
        ticket = make_ticket("T001")
        del ticket["status"]
        with self.assertRaises(ValueError):
            build_report([ticket])

    def test_missing_priority_raises_value_error(self):
        ticket = make_ticket("T001")
        del ticket["priority"]
        with self.assertRaises(ValueError):
            build_report([ticket])

    def test_wrong_case_values_raise(self):
        with self.assertRaises(ValueError):
            build_report([make_ticket("T001", "Open", "low")])
        with self.assertRaises(ValueError):
            build_report([make_ticket("T002", "open", "HIGH")])

    def test_none_and_non_string_values_raise(self):
        with self.assertRaises(ValueError):
            build_report([make_ticket("T001", None, "low")])
        with self.assertRaises(ValueError):
            build_report([make_ticket("T002", ["open"], "low")])

    def test_error_message_names_the_ticket(self):
        with self.assertRaises(ValueError) as ctx:
            build_report([make_ticket("T007", "banana", "low")])
        self.assertIn("T007", str(ctx.exception))

    def test_bad_ticket_after_good_ones_still_raises(self):
        tickets = [
            make_ticket("T001", "open", "low"),
            make_ticket("T002", "banana", "low"),
        ]
        with self.assertRaises(ValueError):
            build_report(tickets)

    def test_report_works_with_real_created_tickets(self):
        tickets = []
        create_ticket(tickets, "Server Down", "Network", "high", 15)
        create_ticket(tickets, "Projector", "Other", "low", 1)
        report = build_report(tickets)
        self.assertEqual(report["total"], 2)
        self.assertEqual(report["by_status"]["open"], 2)
        self.assertEqual(report["by_priority"]["critical"], 1)
        self.assertEqual(report["by_priority"]["low"], 1)


if __name__ == "__main__":
    unittest.main()