from models.models import db, User, ToDoList
from models.models import Task, TaskStatus, Permission, shared_lists
from flask import Flask, request, jsonify, abort
from flask_migrate import Migrate
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from . import todo_blueprint


@todo_blueprint.route('/todolists', methods=['POST'])
@jwt_required()
def create_todolist():
    """
    Create a new ToDoList.
    Requires JSON input with 'title' and optionally 'user_id'.
    Returns the created ToDoList with its ID and title.
    """
    data = request.json
    new_list = ToDoList(title=data['title'], user_id=data.get('user_id'))
    db.session.add(new_list)
    db.session.commit()
    return jsonify({'id': new_list.id, 'title': new_list.title}), 201


@todo_blueprint.route('/todolists', methods=['GET'])
@jwt_required()
def get_todolists():
    """
    Retrieve all ToDoList items associated with the current authenticated user.
    Returns a list of ToDoList items including their IDs and titles.
    """
    user_id = get_jwt_identity()

    # Filter ToDoList items by user_id
    lists = ToDoList.query.filter_by(user_id=user_id).all()
    return jsonify([{'id': lst.id, 'title': lst.title} for lst in lists]), 200


@todo_blueprint.route('/all-todolists', methods=['GET'])
@jwt_required()
def get_all_todolists():
    """
    Retrieve all ToDoList items from the database.
    Returns a list of all ToDoList items including their IDs and titles.
    This route does not filter by user and is intended for administrative purposes.
    """
    lists = ToDoList.query.all()
    return jsonify([{'id': lst.id, 'title': lst.title} for lst in lists]), 200

@jwt_required()
@todo_blueprint.route('/todolists/<int:list_id>', methods=['GET'])
def get_todolist(list_id):
    """
    Retrieve a specific ToDoList by its ID.
    The route parameter 'list_id' specifies the ID of the ToDoList to retrieve.
    Returns the ToDoList item including its ID and title.
    """
    list = db.session.get(ToDoList, list_id)
    if list is None:
        abort(404, 'User does not exist')
    return jsonify({'id': list.id, 'title': list.title}), 200


@jwt_required()
@todo_blueprint.route('/todolists/<int:list_id>', methods=['PUT'])
def update_todolist(list_id):
    """
    Update the title of an existing ToDoList.
    Requires JSON input with the new 'title'.
    The route parameter 'list_id' specifies the ID of the ToDoList to update.
    Returns the updated ToDoList item including its ID and title.
    """
    todolist = db.session.get(ToDoList, list_id)
    if todolist is None:
        abort(404, 'User does not exist')
    data = request.json
    todolist.title = data.get('title', todolist.title)
    db.session.commit()
    return jsonify({'id': todolist.id, 'title': todolist.title}), 200

@jwt_required()
@todo_blueprint.route('/todolists/<int:list_id>', methods=['DELETE'])
def delete_todo_list(list_id):
    todolist = db.session.get(ToDoList, list_id)
    if todolist is None:
        abort(404)
    db.session.delete(todolist)
    db.session.commit()
    return jsonify({'message': 'Todo list deleted'}), 200



@todo_blueprint.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    """
    Create a new task associated with a ToDoList.
    Requires JSON input with 'description', 'status', 'due_date', and 'list_id'.
    Returns the created Task with its ID.
    """
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
    """
    Update details of an existing task.
    Requires JSON input with 'description', 'status', and 'due_date'.
    The route parameter 'task_id' specifies the ID of the Task to update.
    Returns the updated Task details including its ID, description, and status.
    """
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
    """
    Share a ToDoList with another user.
    Requires JSON input with 'list_id', 'share_with_username', and 'permission'.
    Validates the ownership of the ToDoList before sharing.
    Returns a confirmation message upon successful sharing.
    """
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
