import unittest
from app import create_app, db
from models.models import User
from werkzeug.security import generate_password_hash, check_password_hash

class AuthTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_registration(self):
        response = self.client.post('/users', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('testuser', response.get_json()['username'])

    def test_user_login(self):
        # First, create a user
        hashed_password = generate_password_hash('testpassword')
        user = User(username='testuser', password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()

        # breakpoint()
        response = self.client.post('/login', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.get_json())
