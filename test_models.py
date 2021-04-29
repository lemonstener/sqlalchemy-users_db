from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users_db_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    """Tests for the User model."""

    def setUp(self):
        """Clean up any existing users"""

        User.query.delete()

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_fullname(self):
        '''Test the full_name() function.'''
        user = User(first_name="John", last_name="Doe")
        self.assertEqual(user.full_name(), "John Doe")

    def test_image_url(self):
        '''Make sure default image works.'''
        user = User(first_name="John", last_name="Doe")
        db.session.add(user)
        db.session.commit()
        self.assertEquals(user.image_url,'https://www.travelcontinuously.com/wp-content/uploads/2018/04/empty-avatar.png')

       