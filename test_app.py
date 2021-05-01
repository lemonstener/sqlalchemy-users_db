from unittest import TestCase

from app import app
from models import db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users_db_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

class UserViewsTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """Drop and create all tables, add sample user."""

        db.drop_all()
        db.create_all()

        user = User(first_name="John", last_name='Doe')
        db.session.add(user)
        db.session.commit()

        post = Post(title='Hi',content='Bye',user_id=1)
        db.session.add(post)
        db.session.commit()


        self.user_id = user.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_home_page(self):
        with app.test_client() as client:
            '''Test the home page.'''

            res = client.get("/")
            html = res.get_data(as_text=True)
            
            ''' / redirects to /users.'''
            self.assertEqual(res.status_code, 302)
    
    def test_home_page_followed(self):
        with app.test_client() as client:
            '''Redirection from home page followed.'''

            res = client.get("/", follow_redirects=True)
            html = res.get_data(as_text=True)
            
            
            self.assertEqual(res.status_code, 200)
            '''Tests that /users shows a list of all users'''
            self.assertIn('<li><a href="/users/1">John Doe</a></li>',html)
            

    def test_show_user(self):
        '''Tests the user page, make sure it displays the only right user and correct posts.'''
        with app.test_client() as client:
            res = client.get("/users/1")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>John Doe</h1>',html)

            '''User page displays all of the user's posts'''
            self.assertIn('<li><a href="/posts/1">Hi</a></li>',html)
    
    def test_new_user(self):
        '''New user redirection test'''
        with app.test_client() as client:
            res = client.post('/users/new',data={'first':'Jane','last':'Smith','url':''})
            
            self.assertEqual(res.status_code,302)
            self.assertEqual(res.location,'http://localhost/users')
    
    def test_new_user_followed_success(self):
        with app.test_client() as client:
            res = client.post('/users/new',data={'first':'Jane','last':'Smith','url':''}, follow_redirects=True)
            html = res.get_data(as_text=True)
            
            '''Test for a successfull creation of new user'''
            self.assertEqual(res.status_code,200)
            self.assertIn('Jane Smith',html)

    def test_new_user_followed_fail(self):
        with app.test_client() as client:
            res = client.post('/users/new',data={'first':'Jane','last':'','url':''}, follow_redirects=True)
            html = res.get_data(as_text=True)
            
            '''Test for failed new user creation, make sure page doesn't break, display flash messages'''
            self.assertEqual(res.status_code,200)
            self.assertNotIn('Jane',html)
            self.assertIn('<p>First and last names cannot be empty</p>',html)
    
    
    def test_post_page(self):
        with app.test_client() as client:
            '''Test a post's "home" page'''
            res = client.get('/posts/1')
            html = res.get_data(as_text=True)

            self.assertIn('<h1>Hi</h1>',html)
            self.assertIn('<p>Bye</p>',html)
            self.assertIn('<blockquote>By John Doe</blockquote>',html)

    def test_new_post(self):
        with app.test_client() as client:
            res = client.post('/users/1/posts/new',data={'title':'Hello','content':'Goodbye'})

            self.assertEqual(res.status_code,302)
            self.assertEqual(res.location,'http://localhost/users/1')
    
    def test_new_post_followed_success(self):
        with app.test_client() as client:
            res = client.post('/users/1/posts/new',data={'title':'Hello','content':'Goodbye'}, follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code,200)
            self.assertIn('Hello',html)

    def test_new_post_followed_fail(self):
        with app.test_client() as client:
            res = client.post('/users/1/posts/new',data={'title':'Hello','content':''}, follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code,200)
            self.assertNotIn('Hello',html)
    
    def test_delete_user(self):
        with app.test_client() as client:
            res = client.get('/users/1/delete')
            
            '''Test redirection'''
            self.assertEqual(res.status_code,302)
            self.assertEqual(res.location,'http://localhost/users')

    def test_delete_user_followed(self):
        with app.test_client() as client:
            res = client.get('/users/1/delete', follow_redirects=True)
            html = res.get_data(as_text=True)
            
            self.assertEqual(res.status_code,200)
            self.assertNotIn('<h1>John Doe</h1>',html)
    
    def test_delete_post(self):
        with app.test_client() as client:
            res = client.get('/posts/1/delete')
        
        '''Test redirection'''
        self.assertEqual(res.status_code,302)
        self.assertEqual(res.location,'http://localhost/users/1')

    def test_delete_post_followed(self):
        with app.test_client() as client:
            res = client.get('/posts/1/delete', follow_redirects=True)
            html = res.get_data(as_text=True)
        
        '''Make sure post is deleted, make sure it does not affect the user aside from the list contents.'''
        self.assertEqual(res.status_code,200)
        self.assertNotIn('<h1>Hi</h1>',html)
        self.assertIn('<h1>John Doe</h1>',html)

