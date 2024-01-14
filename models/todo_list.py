from app import db

class ToDoList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tasks = db.relationship('Task', backref='todolist', lazy=True)

    def __repr__(self):
        return f'<ToDoList {self.title}>'
