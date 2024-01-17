import unittest
from app import create_app, db
from models.models import User, ToDoList, Task
from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token

class ToDoTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

        # Create a test user and a test todo list
        user = User(username='testuser', password_hash=generate_password_hash('test'))
        db.session.add(user)
        db.session.commit()

        self.test_user_id = user.id
        self.test_todo_list = ToDoList(title='Test ToDo List', user_id=self.test_user_id)
        db.session.add(self.test_todo_list)
        db.session.commit()

        self.token = create_access_token(identity='testuser')

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_todolist(self):
        response = self.client.post('/todolists', json={'title': 'New ToDo List', 'user_id': 1},
                                    headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(response.status_code, 201)
        self.assertIn('New ToDo List', response.get_json()['title'])

    def test_get_todolist(self):
        response = self.client.get(f'/todolists/{self.test_todo_list.id}',
                                   headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test ToDo List', response.get_json()['title'])

