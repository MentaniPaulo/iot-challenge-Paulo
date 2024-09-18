import unittest
from datetime import datetime
from record_api.record import filter_camera_data  # Adjust the import as needed

class TestFilterCameraData(unittest.TestCase):

    def setUp(self):
        self.data = {
            "result": "success",
            "data": {
                "record": [[
                    {"record_type": 1, "start_time": "00:10:00", "end_time": "00:20:00"},
                    {"record_type": 1, "start_time": "00:25:00", "end_time": "00:30:00"},
                    {"record_type": 2, "start_time": "00:35:00", "end_time": "00:40:00"},
                    {"record_type": 1, "start_time": "00:45:00", "end_time": "00:50:00"}
                ]]
            }
        }

    def test_filter_valid_records(self):
        result = filter_camera_data(self.data, "00:00:00", "00:30:00", 1)
        expected = [
            {"record_type": 1, "start_time": "00:10:00", "end_time": "00:20:00"},
            {"record_type": 1, "start_time": "00:25:00", "end_time": "00:30:00"}
        ] 
        self.assertEqual(result, expected)

    def test_filter_no_records(self):
        result = filter_camera_data(self.data, "00:00:00", "00:09:00", 1)
        self.assertEqual(result, [])

    def test_filter_invalid_data(self):
        result = filter_camera_data({"result": "failure"}, "00:00:00", "00:30:00", 1) 
        self.assertEqual(result, [])

    def test_filter_time_range(self):
        result = filter_camera_data(self.data, "00:00:00", "00:40:00", 1)
        expected = [
            {"record_type": 1, "start_time": "00:10:00", "end_time": "00:20:00"},
            {"record_type": 1, "start_time": "00:25:00", "end_time": "00:30:00"}
        ] 
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
