import unittest


from app import create_app, db
from app.geocoding import ors_client, ors_profile, ors_preference
from app.models import Marker
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class GeocodingModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_search(self):
        marker = Marker(name="Marker", address="Grenoble, France")
        marker.longitude, marker.latitude = ors_client.search(marker.address)

        self.assertEqual(marker.latitude, 45.177879)
        self.assertEqual(marker.longitude, 5.718545)

    def test_elevation(self):
        marker = Marker(name="Marker_1", latitude=45.177879, longitude=5.718545)
        marker.elevation = ors_client.elevation(marker.latitude, marker.longitude)

        self.assertEqual(marker.elevation, 221)

    def test_direction(self):
        marker_1 = Marker(name="Marker_1", latitude=45.177879, longitude=5.718545)
        marker_2 = Marker(name="Marker_2", latitude=47.058606, longitude=-0.883084)

        path, distance, ascent, descent = ors_client.directions([marker_1, marker_2], ors_profile['Cycling'], ors_preference['Shortest'])

        self.assertEqual(distance, 614127.0)
        self.assertEqual(ascent, 5487.2)
        self.assertEqual(descent, 5624.1)