from flask import Blueprint

todo_blueprint = Blueprint('todo', __name__)

from . import routes
