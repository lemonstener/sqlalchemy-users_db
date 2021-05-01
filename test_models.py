from unittest import TestCase

from app import app
from models import db, User, Post


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users_db_test'
app.config['SQLALCHEMY_ECHO'] = False


class UserPostModelsTestCase(TestCase):
    """Tests for the User model."""

    def setUp(self):
        """Clean up any existing users"""
        db.drop_all()
        db.create_all()

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_user(self):
        '''Multitude of different tests on the User model'''
        user = User(first_name="John", last_name="Doe")
        db.session.add(user)
        db.session.commit()

        '''Test the full_name() function.'''
        self.assertEqual(user.full_name(), "John Doe")

        '''Test for default values'''
        self.assertEqual(user.id, 1)
        self.assertEqual(user.image_url,'https://www.travelcontinuously.com/wp-content/uploads/2018/04/empty-avatar.png')

    def test_user_relation(self):
        '''Tests that the post belongs to right user'''
        user = User(first_name="John",last_name='Doe')
        db.session.add(user)
        db.session.commit()

        post = Post(title="Hi",content="Bye",user_id=1)
        db.session.add(post)
        db.session.commit()
        
        '''Testing happens through the backref property'''
        self.assertEqual(post.user.first_name, 'John')
        self.assertEqual(post.user.id, 1)
    
        
    
    

    

