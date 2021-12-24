import unittest


from app import create_app, db
from app.models import Marker
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class MarkerModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_add_marker(self):
        marker = Marker(name='Marker')
        db.session.add(marker)
        db.session.commit()

        self.assertEqual(Marker.query.count(), 1)

    def test_delete_marker(self):
        marker = Marker(name='Marker')
        db.session.add(marker)
        db.session.commit()

        marker = Marker.query.first()
        db.session.delete(marker)
        db.session.commit()

        self.assertEqual(Marker.query.count(), 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
