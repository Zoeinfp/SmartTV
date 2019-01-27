"""File containing all the unit tests for the application"""

import unittest

from app import app
from helpers import save_image, get_or_create_message_data, get_or_create_event, get_or_create_weather_data, zodiac


class TestFlaskApp(unittest.TestCase):
    """Unit test class to test the App """

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_home(self):
        rv = self.app.get('/')
        self.assertFalse((rv.status_code == 302 or rv.status_code == 200))

    def test_weather_by_url(self):
        rv = self.app.get('/add_weather')
        self.assertTrue((rv.status_code == 302 or rv.status_code == 200))

    def test_save_image(self):
        result = save_image('image')
        self.assertEqual(result, True)

    def test_get_or_create_message_data(self):
        result = get_or_create_message_data('Message')
        self.assertTrue(result)

    def test_get_or_create_event(self):
        result = get_or_create_event('Event')
        self.assertTrue(result, 'Event')

    def test_get_or_create_weather_data(self):
        result = get_or_create_weather_data(name="Nantes", temperature="10", description="Cloudy", icon="None")
        self.assertTrue(result)

    def test_zodiac(self):
        result = zodiac()
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
