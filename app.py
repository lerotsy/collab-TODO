from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models.todo_list import ToDoList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo-app.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

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


if __name__ == '__main__':
    app.run(debug=True)

