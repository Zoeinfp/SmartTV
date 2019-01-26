"""File containing all the unit tests for the application"""

import unittest
from app import app


class TestFlaskApp(unittest.TestCase):
    """Unit test class to test the App """

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_index_by_default_url(self):
        rv = self.app.get('/')
        self.assertEqual(rv.status_code, 200)

    def test_weather_by_url(self):
        rv = self.app.get('/update_weather')
        self.assertEqual(rv.status_code, 200)


if __name__ == "__main__":
    unittest.main()
