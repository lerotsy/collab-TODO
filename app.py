from models.models import db, User, ToDoList
from models.models import Task, TaskStatus, Permission, shared_lists
from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from blueprints.auth import auth_blueprint
from blueprints.todo import todo_blueprint
from config import DevelopmentConfig


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(todo_blueprint)

    db.init_app(app)
    migrate = Migrate(app, db)

    jwt = JWTManager(app)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
