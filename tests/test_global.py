import unittest


from faker import Faker


from app import create_app, db
from app.models import User, Trek, Route, RouteMarker, Marker, Profile, Preference
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        Profile.insert_modes()
        Preference.insert_options()

        self.fake = Faker()
        username = self.fake.user_name()
        email = self.fake.email()
        password = self.fake.password()

        self.user = User(username=username, email=email)
        self.user.set_password(password)

        self.trek = Trek(name='Trek')

        self.route_1 = Route(trek=self.trek)
        self.route_2 = Route(trek=self.trek)

        self.marker_1 = Marker(name='Marker_1', user=self.user)
        self.marker_2 = Marker(name='Marker_2', user=self.user)
        
        self.user.treks.append(self.trek)
        self.trek.routes.append(self.route_1)
        self.trek.routes.append(self.route_2)

        self.route_1.markers.append(self.marker_1)
        self.route_1.markers.append(self.marker_2)
        self.route_2.markers.append(self.marker_1)
        self.route_2.markers.append(self.marker_2)

        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_add_global(self):
        self.assertEqual(User.query.count(), 1)
        self.assertEqual(Trek.query.count(), 1)
        self.assertEqual(Route.query.count(), 2)
        self.assertEqual(RouteMarker.query.count(), 4)
        self.assertEqual(Marker.query.count(), 2)

    def test_delete_user(self):
        db.session.delete(self.user)
        db.session.commit()

        self.assertEqual(User.query.count(), 0)
        self.assertEqual(Trek.query.count(), 0)
        self.assertEqual(Route.query.count(), 0)
        self.assertEqual(RouteMarker.query.count(), 0)
        self.assertEqual(Marker.query.count(), 0)

    def test_delete_trek(self):
        db.session.delete(self.trek)
        db.session.commit()

        self.assertEqual(User.query.count(), 1)
        self.assertEqual(Trek.query.count(), 0)
        self.assertEqual(Route.query.count(), 0)
        self.assertEqual(RouteMarker.query.count(), 0)
        self.assertEqual(Marker.query.count(), 2)

    def test_delete_route(self):
        db.session.delete(self.route_1)
        db.session.commit()

        self.assertEqual(User.query.count(), 1)
        self.assertEqual(Trek.query.count(), 1)
        self.assertEqual(Route.query.count(), 1)
        self.assertEqual(RouteMarker.query.count(), 2)
        self.assertEqual(Marker.query.count(), 2)

    def test_delete_routes(self):
        db.session.delete(self.route_1)
        db.session.delete(self.route_2)
        db.session.commit()

        self.assertEqual(User.query.count(), 1)
        self.assertEqual(Trek.query.count(), 1)
        self.assertEqual(Route.query.count(), 0)
        self.assertEqual(RouteMarker.query.count(), 0)
        self.assertEqual(Marker.query.count(), 2)

    def test_delete_marker(self):
        db.session.delete(self.marker_1)
        db.session.commit()

        self.assertEqual(User.query.count(), 1)
        self.assertEqual(Trek.query.count(), 1)
        self.assertEqual(Route.query.count(), 2)
        self.assertEqual(RouteMarker.query.count(), 2)
        self.assertEqual(Marker.query.count(), 1)

    def test_delete_markers(self):
        db.session.delete(self.marker_1)
        db.session.delete(self.marker_2)
        db.session.commit()

        self.assertEqual(User.query.count(), 1)
        self.assertEqual(Trek.query.count(), 1)
        self.assertEqual(Route.query.count(), 2)
        self.assertEqual(RouteMarker.query.count(), 0)
        self.assertEqual(Marker.query.count(), 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
