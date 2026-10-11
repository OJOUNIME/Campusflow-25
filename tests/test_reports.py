import copy
import unittest

from campusflow.reports import build_report


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
            make_ticket("T1", "open", "critical"),
            make_ticket("T2", "open", "low"),
            make_ticket("T3", "in_progress", "high", "Ana"),
            make_ticket("T4", "resolved", "high", "Ben"),
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
        report = build_report([make_ticket("T1", "open", "low")])
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
            make_ticket("T1", "open", "critical"),
            make_ticket("T2", "resolved", "medium"),
            make_ticket("T3", "in_progress", "low", "Ana"),
        ]
        report = build_report(tickets)
        self.assertEqual(sum(report["by_status"].values()), report["total"])
        self.assertEqual(sum(report["by_priority"].values()), report["total"])

    def test_unknown_status_raises(self):
        with self.assertRaises(ValueError):
            build_report([make_ticket("T1", "banana", "low")])

    def test_unknown_priority_raises(self):
        with self.assertRaises(ValueError):
            build_report([make_ticket("T1", "open", "urgent")])

    def test_does_not_modify_input(self):
        tickets = [
            make_ticket("T1", "open", "high"),
            make_ticket("T2", "resolved", "low"),
        ]
        snapshot = copy.deepcopy(tickets)
        build_report(tickets)
        self.assertEqual(tickets, snapshot)


if __name__ == "__main__":
    unittest.main()