from app import db

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
