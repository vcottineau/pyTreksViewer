import unittest


from faker import Faker


from app import create_app, db
from app.models import User, Trek, Route, Marker, Mode, Option
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

        Mode.insert_modes()
        Option.insert_options()

        self.fake = Faker()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_add_user(self):
        username = self.fake.user_name()
        email = self.fake.email()
        password = self.fake.password()

        user = User(username=username, email=email)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        self.assertEqual(User.query.count(), 1)

    def test_delete_user(self):
        username = self.fake.user_name()
        email = self.fake.email()
        password = self.fake.password()

        user = User(username=username, email=email)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        user = User.query.first()
        db.session.delete(user)

        self.assertEqual(User.query.count(), 0)

    def test_add_trek(self):
        username = self.fake.user_name()
        email = self.fake.email()
        password = self.fake.password()

        user = User(username=username, email=email)
        user.set_password(password)
        trek = Trek(name='Trek_1', user=user)

        db.session.add(user)
        db.session.add(trek)
        db.session.commit()

        self.assertEqual(User.query.count(), 1)
        self.assertEqual(Trek.query.count(), 1)
        self.assertEqual(user.treks.count(), 1)

    def test_delete_trek(self):
        username = self.fake.user_name()
        email = self.fake.email()
        password = self.fake.password()

        user = User(username=username, email=email)
        user.set_password(password)
        trek = Trek(name='Trek_1', user=user)

        db.session.add(user)
        db.session.add(trek)
        db.session.commit()

        db.session.delete(trek)
        db.session.commit()

        self.assertEqual(User.query.count(), 1)
        self.assertEqual(Trek.query.count(), 0)
        self.assertEqual(user.treks.count(), 0)


class TrekModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        Mode.insert_modes()
        Option.insert_options()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_add_trek(self):
        trek = Trek(name='Trek_1')
        db.session.add(trek)
        db.session.commit()

        self.assertEqual(Trek.query.count(), 1)

    def test_delete_trek(self):
        trek = Trek(name='Trek_1')
        db.session.add(trek)
        db.session.commit()

        trek = Trek.query.first()
        db.session.delete(trek)
        db.session.commit()

        self.assertEqual(Trek.query.count(), 0)

    def test_add_marker(self):
        trek = Trek(name='Trek_1')
        marker = Marker(name='Marker_1')
        trek.add_marker(marker)
        self.assertEqual(trek.markers.count(), 1)

    def test_delete_marker(self):
        trek = Trek(name='Trek_1')
        marker = Marker(name='Marker_1')
        trek.add_marker(marker)
        db.session.commit()

        trek.remove_marker(marker)
        self.assertEqual(trek.markers.count(), 0)

    def test_mode(self):
        trek = Trek(name='Trek_1')
        trek.mode = Mode.query.filter_by(default=True).first()
        self.assertEqual(trek.mode.name, 'Cycling')

    def test_option(self):
        trek = Trek(name='Trek_1')
        trek.option = Option.query.filter_by(default=True).first()
        self.assertEqual(trek.option.name, 'Shortest')


class RouteModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        Mode.insert_modes()
        Option.insert_options()

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
        start_marker = Marker(name='Marker_1')
        end_marker = Marker(name='Marker_2')

        route = Route(start_marker=start_marker, end_marker=end_marker)

        db.session.add(route)
        db.session.commit()

        self.assertEqual(Route.query.count(), 1)
        self.assertEqual(Marker.query.count(), 2)

        self.assertEqual(route.start_marker, start_marker)
        self.assertEqual(route.end_marker, end_marker)
        self.assertEqual(start_marker.start_markers.count(), 1)
        self.assertEqual(end_marker.end_markers.count(), 1)
        

class MarkerModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        Mode.insert_modes()
        Option.insert_options()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_add_marker(self):
        marker = Marker(name='Marker_1')
        db.session.add(marker)
        db.session.commit()

        self.assertEqual(Marker.query.count(), 1)

    def test_delete_marker(self):
        marker = Marker(name='Marker_1')
        db.session.add(marker)
        db.session.commit()

        marker = Marker.query.first()
        db.session.delete(marker)
        db.session.commit()

        self.assertEqual(Marker.query.count(), 0)

    def test_add_trek(self):
        trek_1 = Trek(name='Trek_1')
        trek_2 = Trek(name='Trek_2')
        marker = Marker(name='Marker_1')
        trek_1.add_marker(marker)
        trek_2.add_marker(marker)

        self.assertEqual(marker.treks.count(), 2)

    def test_delete_trek(self):
        trek_1 = Trek(name='Trek_1')
        trek_2 = Trek(name='Trek_2')
        marker = Marker(name='Marker_1')
        trek_1.add_marker(marker)
        trek_2.add_marker(marker)
        db.session.commit()

        trek_1.remove_marker(marker)
        self.assertEqual(marker.treks.count(), 1)


if __name__ == '__main__':
    unittest.main(verbosity=2)