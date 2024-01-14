# Flask Model Creation Cheat Sheet

# Import SQLAlchemy and Create Database Instance
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# Basic Model Structure
class MyModel(db.Model):
    __tablename__ = 'my_table'
    # Add fields and relationships here

# Fields/Columns Definitions

# Primary Key Field
id = db.Column(db.Integer, primary_key=True)

# String Field
name = db.Column(db.String(120), nullable=False)

# Integer Field
age = db.Column(db.Integer)

# DateTime Field with Default Current Timestamp
created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

# Boolean Field
is_active = db.Column(db.Boolean, default=True)

# Enum Field
from enum import Enum
class MyEnum(Enum):
    TYPE1 = 1
    TYPE2 = 2
enum_field = db.Column(db.Enum(MyEnum))

# Relationships Definitions

# One-to-Many Relationship
class ParentModel(db.Model):
    children = db.relationship('ChildModel', backref='parent', lazy=True)

class ChildModel(db.Model):
    parent_id = db.Column(db.Integer, db.ForeignKey('parent_model.id'))

# Many-to-Many Relationship
association_table = db.Table('association',
    db.Column('left_id', db.Integer, db.ForeignKey('left.id')),
    db.Column('right_id', db.Integer, db.ForeignKey('right.id'))
)

class LeftModel(db.Model):
    rights = db.relationship('RightModel', secondary=association_table, back_populates='lefts')

class RightModel(db.Model):
    lefts = db.relationship('LeftModel', secondary=association_table, back_populates='rights')

# Miscellaneous Model Features

# Custom Methods in Model
def example_method(self):
    # Custom method logic
    pass

# Model Inheritance
class Base(db.Model):
    __abstract__ = True
    # Common fields here

class Child(Base):
    # Child-specific fields

# Serialization Method
def serialize(self):
    return {
        'field1': self.field1,
        'field2': self.field2,
        # Add other fields
    }

# Using the Models in Flask

# Initialize Flask App and SQLAlchemy
from flask import Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db.init_app(app)

# Creating Tables in Database
with app.app_context():
    db.create_all()

# Adding Records to Database
new_record = MyModel(name='Sample', age=30)
db.session.add(new_record)
db.session.commit()

# Querying Records from Database
records = MyModel.query.all()  # Get all records
record = MyModel.query.filter_by(name='Sample').first()  # Get first record with name 'Sample'

# Updating Records in Database
record = MyModel.query.get(record_id)
if record:
    record.name = 'New Name'
    db.session.commit()

# Deleting Records from Database
record = MyModel.query.get(record_id)
if record:
    db.session.delete(record)
    db.session.commit()

# Additional Tips

# Define __repr__ Method for Models
def __repr__(self):
    return f'<MyModel {self.name}>'

# Optimize Queries and Be Cautious with User Input to Prevent SQL Injection
# Consider Using Flask-Migrate for Database Migrations
