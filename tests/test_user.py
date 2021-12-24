import unittest


from faker import Faker


from app import create_app, db
from app.models import User
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


if __name__ == '__main__':
    unittest.main(verbosity=2)
