import unittest
from datetime import datetime
from record_api.record import check_parameters_integrity

class TestCheckParametersIntegrity(unittest.TestCase):

    def test_valid_times(self):
        self.assertFalse(check_parameters_integrity("12:00:00", "13:00:00"))  # Valid times
        self.assertFalse(check_parameters_integrity("00:00:00", "23:59:59"))  # Valid times

    def test_invalid_times_format(self):
        self.assertTrue(check_parameters_integrity("12:00", "13:00:00"))   # Invalid format for start_time
        self.assertTrue(check_parameters_integrity("12:00:00", "13:00"))   # Invalid format for end_time
        self.assertTrue(check_parameters_integrity("25:00:00", "13:00:00")) # Invalid hour in start_time

    def test_start_time_after_end_time(self):
        self.assertTrue(check_parameters_integrity("14:00:00", "13:00:00"))  # Start time is not less than end time

if __name__ == '__main__':
    unittest.main()
