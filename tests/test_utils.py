import unittest
from app.utils import get_deviation_status
from app.utils import generate_unique_id


class TestUtils(unittest.TestCase):
    def test_generate_unique_id(self):
        unique_id = generate_unique_id("2022-04-30", "45.678", "-122.789")
        self.assertIsInstance(unique_id, str)
        self.assertEqual(len(unique_id), 64)  # SHA-256 hash length
        self.assertEqual(unique_id, "d69e4b1df76d261b4e3b244083320661b9130c9230ac04d5da194f1ae1bb0783")

    def test_get_deviation_status(self):
        status1 = get_deviation_status(max_temp=30, min_temp=10, max_limit=25, min_limit=15)
        self.assertEqual(status1, "increased&decreased")

        status2 = get_deviation_status(max_temp=25, min_temp=18, max_limit=20, min_limit=15)
        self.assertEqual(status2, "increased")

        status3 = get_deviation_status(max_temp=30, min_temp=10, max_limit=35, min_limit=15)
        self.assertEqual(status3, "decreased")

        status4 = get_deviation_status(max_temp=25, min_temp=18, max_limit=30, min_limit=15)
        self.assertEqual(status4, "normal")

if __name__ == '__main__':
    unittest.main()

