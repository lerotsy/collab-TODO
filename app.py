from models.models import db
from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token
from blueprints.auth import auth_blueprint
from blueprints.todo import todo_blueprint
from config import DevelopmentConfig, ProductionConfig, TestingConfig
from flask_cors import CORS


def create_app(config_name='dev'):
    app = Flask(__name__)
    CORS(app)
    if config_name == 'prod':
        app.config.from_object(ProductionConfig)
    elif config_name == 'test':
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(todo_blueprint)

    db.init_app(app)
    Migrate(app, db)
    JWTManager(app)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
