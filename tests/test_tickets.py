
import unittest
from campusflow.tickets import calculate_priority


class TestCalculatePriority(unittest.TestCase):

    def test_high_and_many_users(self):
        self.assertEqual(calculate_priority("high", 12), "critical")

    def test_high_and_few_users(self):
        self.assertEqual(calculate_priority("high", 2), "high")

    def test_low_and_four_users(self):
        self.assertEqual(calculate_priority("low", 4), "medium")

    def test_low_and_one_user(self):
        self.assertEqual(calculate_priority("low", 1), "low")

    # Boundary tests
    def test_nine_users(self):
        self.assertEqual(calculate_priority("low", 9), "medium")

    def test_ten_users(self):
        self.assertEqual(calculate_priority("low", 10), "high")

    def test_two_users(self):
        self.assertEqual(calculate_priority("low", 2), "low")

    def test_three_users(self):
        self.assertEqual(calculate_priority("low", 3), "medium")


if __name__ == "__main__":
    unittest.main()
