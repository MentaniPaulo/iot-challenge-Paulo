import unittest
from record_api.record import check_time_integrity
 
class TestCheckTimeIntegrity(unittest.TestCase):

    def test_valid_date(self):
        self.assertFalse(check_time_integrity(5, 15))  # Valid month and day
        self.assertFalse(check_time_integrity(12, 31))  # Valid month and day

    def test_invalid_month(self):
        self.assertTrue(check_time_integrity(0, 15))   # Invalid month
        self.assertTrue(check_time_integrity(13, 15))  # Invalid month

    def test_invalid_day(self):
        self.assertTrue(check_time_integrity(5, 0))    # Invalid day
        self.assertTrue(check_time_integrity(5, 32))   # Invalid day

if __name__ == '__main__':
    unittest.main()
