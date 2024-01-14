from app import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    list_id = db.Column(db.Integer, db.ForeignKey('to_do_list.id'), nullable=False)

    def __repr__(self):
        return f'<Task {self.description}>'
