import unittest


from faker import Faker


from app import create_app, db
from app.models import Route, Marker, Profile, Preference
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class RouteModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        Profile.insert_modes()
        Preference.insert_options()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_add_route(self):
        route = Route()
        db.session.add(route)
        db.session.commit()

        self.assertEqual(Route.query.count(), 1)

    def test_delete_route(self):
        route = Route()
        db.session.add(route)
        db.session.commit()

        route = Route.query.first()
        db.session.delete(route)
        db.session.commit()

        self.assertEqual(Route.query.count(), 0)

    def test_add_marker(self):
        route = Route()
        marker = Marker(name='Marker')
        route.markers.append(marker)

        db.session.add(route)
        db.session.commit()

        self.assertEqual(len(route.markers), 1)

    def test_update_marker(self):
        route = Route()
        marker_1 = Marker(name='Marker_1')
        marker_2 = Marker(name='Marker_2')
        route.markers.append(marker_1)
        route.markers.append(marker_2)

        db.session.add(route)
        db.session.commit()

        route.markers.remove(marker_2)
        route.markers.insert(0, marker_2)

        self.assertEqual(route.markers[0], marker_2)
        self.assertEqual(route.markers[1], marker_1)

    def test_delete_marker(self):
        route = Route()
        marker = Marker(name='Marker')
        route.markers.append(marker)

        db.session.add(route)
        db.session.commit()

        route.markers.remove(marker)
        self.assertEqual(len(route.markers), 0)

    def test_mode(self):
        route = Route()
        route.profile = Profile.query.filter_by(default=True).first()
        self.assertEqual(route.profile.name, 'Cycling')

    def test_option(self):
        route = Route()
        route.preference = Preference.query.filter_by(default=True).first()
        self.assertEqual(route.preference.name, 'Shortest')


if __name__ == '__main__':
    unittest.main(verbosity=2)
