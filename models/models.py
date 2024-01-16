# from app import db
from flask_sqlalchemy import SQLAlchemy
import enum


class TaskStatus(enum.Enum):
    NEW = 'new'
    STARTED = 'started'
    COMPLETED = 'completed'


class Permission(enum.Enum):
    READ = 'read'
    WRITE = 'write'
    ADMIN = 'admin'


db = SQLAlchemy()

shared_lists = db.Table('shared_lists',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('list_id', db.Integer, db.ForeignKey('to_do_list.id'), primary_key=True),
    db.Column('permissions', db.Enum(Permission), default=Permission.READ)
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    lists = db.relationship('ToDoList', backref='user', lazy=True)
    shared_lists = db.relationship('ToDoList', secondary=shared_lists, 
                                   lazy='subquery', 
                                   backref=db.backref('shared_with', lazy=True))

    def __repr__(self):
        return f'<User {self.username}>'

class ToDoList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, 
                           default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=False, 
                           default=db.func.current_timestamp(),
                           onupdate=db.func.current_timestamp())
    tasks = db.relationship('Task', backref='todolist', lazy=True)

    def __repr__(self):
        return f'<ToDoList {self.title}>'

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.Enum(TaskStatus), default=TaskStatus.NEW)
    due_date = db.Column(db.DateTime)
    list_id = db.Column(db.Integer, db.ForeignKey('to_do_list.id'), nullable=False)

    def __repr__(self):
        return f'<Task {self.description}>'