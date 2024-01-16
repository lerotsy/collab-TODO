from models.models import db, User, ToDoList
from models.models import Task, TaskStatus, Permission, shared_lists
from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from . import todo_blueprint


@todo_blueprint.route('/todolists', methods=['POST'])
@jwt_required()
def create_todolist():
    data = request.json
    new_list = ToDoList(title=data['title'], user_id=data.get('user_id'))
    db.session.add(new_list)
    db.session.commit()
    return jsonify({'id': new_list.id}), 201


@todo_blueprint.route('/todolists', methods=['GET'])
@jwt_required()
def get_todolists():
    lists = ToDoList.query.all()
    return jsonify([{'id': lst.id, 'title': lst.title} for lst in lists]), 200


@todo_blueprint.route('/users', methods=['POST'])
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


@todo_blueprint.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'username': user.username} for user in users]), 200


@todo_blueprint.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({'id': user.id, 'username': user.username}), 200


@todo_blueprint.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.json
    user.username = data.get('username', user.username)
    if 'password' in data:
        user.password_hash = generate_password_hash(data['password'])
    db.session.commit()
    return jsonify({'id': user.id, 'username': user.username}), 200


@todo_blueprint.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'}), 200


@todo_blueprint.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    data = request.get_json()
    new_task = Task(
        description=data['description'],
        status=TaskStatus[data.get('status', 'NEW')],
        due_date=datetime.strptime(data.get('due_date'),
                                   "%Y-%m-%dT%H:%M:%S") if data.get('due_date') else None,
        list_id=data.get('list_id', 1)
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'id': new_task.id}), 201


@todo_blueprint.route('/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json()
    task.description = data.get('description', task.description)
    if 'status' in data:
        task.status = TaskStatus[data['status']]
    task.due_date = data.get('due_date', task.due_date)
    db.session.commit()
    return jsonify({'id': task.id, 'description': task.description, 'status': task.status.name}), 200


@todo_blueprint.route('/share_todo_list', methods=['POST'])
@jwt_required()
def share_todo_list():
    current_user_username = get_jwt_identity()
    data = request.get_json()
    list_id = data.get('list_id')
    share_with_username = data.get('share_with_username')
    permission = data.get('permission', 'READ').upper()

    # Find current user
    current_user = User.query.filter_by(username=current_user_username).first()
    if not current_user:
        return jsonify({'message': 'Current user not found'}), 404

    # Find the list to share
    todo_list = ToDoList.query.get(list_id)
    if not todo_list or todo_list.user_id != current_user.id:
        return jsonify({'message': 'ToDo list not found or not owned by the user'}), 403

    # Find the user to share with
    user_to_share_with = User.query.filter_by(
        username=share_with_username).first()
    if not user_to_share_with:
        return jsonify({'message': 'User to share with not found'}), 404

    # Check if the list is already shared with the user
    is_already_shared = db.session.query(shared_lists).filter_by(
        user_id=user_to_share_with.id,
        list_id=list_id
    ).first() is not None

    if is_already_shared:
        return jsonify(
            {'message': 'ToDo list already shared with this user'}), 400

    # Share the list
    new_shared_list = shared_lists.insert().values(
        user_id=user_to_share_with.id,
        list_id=list_id,
        permissions=Permission[permission]
    )
    db.session.execute(new_shared_list)
    db.session.commit()

    return jsonify({'message': f'ToDo list shared with {share_with_username} with {permission.lower()} permission'}), 200
