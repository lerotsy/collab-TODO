from models.models import  User
from flask import request, jsonify
from werkzeug.security import check_password_hash
from flask_jwt_extended import  create_access_token
from . import auth_blueprint


@auth_blueprint.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token)
    return jsonify({"msg": "Bad username or password"}), 401