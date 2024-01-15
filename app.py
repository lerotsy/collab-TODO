from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models.models import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo-app.db'
app.config['JWT_SECRET_KEY'] = 'mysecretkey'

db.init_app(app)
migrate = Migrate(app, db)

jwt = JWTManager(app)

from models.models import User, ToDoList


@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token)
    return jsonify({"msg": "Bad username or password"}), 401

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/todolists', methods=['POST'])
def create_todolist():
    data = request.json
    new_list = ToDoList(title=data['title'])
    db.session.add(new_list)
    db.session.commit()
    return jsonify({'id': new_list.id}), 201

@app.route('/todolists', methods=['GET'])
def get_todolists():
    lists = ToDoList.query.all()
    return jsonify([{'id': lst.id, 'title': lst.title} for lst in lists]), 200

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    if not data or 'username' not in data or 'password' not in data:
        abort(400, 'Username and password are required.')
    
    # Check if user already exists
    if User.query.filter_by(username=data['username']).first():
        abort(400, 'Username already exists.')

    hashed_password = generate_password_hash(data['password'])
    new_user = User(username=data['username'], password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'id': new_user.id, 'username': new_user.username}), 201

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'username': user.username} for user in users]), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({'id': user.id, 'username': user.username}), 200

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.json
    user.username = data.get('username', user.username)
    if 'password' in data:
        user.password_hash = generate_password_hash(data['password'])
    db.session.commit()
    return jsonify({'id': user.id, 'username': user.username}), 200

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'}), 200


if __name__ == '__main__':
    app.run(debug=True)

