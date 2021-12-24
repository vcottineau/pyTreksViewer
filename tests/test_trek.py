import unittest


from faker import Faker


from app import create_app, db
from app.models import User, Trek, Route, Profile, Preference
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class TrekModelCase(unittest.TestCase):
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

    def test_add_trek(self):
        trek = Trek(name='Trek')
        db.session.add(trek)
        db.session.commit()

        self.assertEqual(Trek.query.count(), 1)

    def test_delete_trek(self):
        trek = Trek(name='Trek')
        db.session.add(trek)
        db.session.commit()

        trek = Trek.query.first()
        db.session.delete(trek)
        db.session.commit()

        self.assertEqual(Trek.query.count(), 0)

    def test_add_route(self):
        trek = Trek(name='Trek')
        route = Route()
        trek.routes.append(route)

        db.session.add(trek)
        db.session.commit()

        self.assertEqual(len(trek.routes), 1)

    def test_update_route(self):
        trek = Trek(name='Trek')
        route_1 = Route()
        route_2 = Route()
        trek.routes.append(route_1)
        trek.routes.append(route_2)

        db.session.add(trek)
        db.session.commit()

        trek.routes.remove(route_2)
        trek.routes.insert(0, route_2)

        self.assertEqual(trek.routes[0], route_2)
        self.assertEqual(trek.routes[1], route_1)

    def test_delete_route(self):
        trek = Trek(name='Trek')
        route = Route()
        trek.routes.append(route)

        db.session.add(trek)
        db.session.commit()

        trek.routes.remove(route)
        self.assertEqual(len(trek.routes), 0)

    def test_mode(self):
        trek = Trek(name='Trek')
        trek.profile = Profile.query.filter_by(default=True).first()
        self.assertEqual(trek.profile.name, 'Cycling')

    def test_option(self):
        trek = Trek(name='Trek')
        trek.preference = Preference.query.filter_by(default=True).first()
        self.assertEqual(trek.preference.name, 'Shortest')


if __name__ == '__main__':
    unittest.main(verbosity=2)