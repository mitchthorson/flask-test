from application import db
from sqlalchemy.dialects.postgresql import JSON

class Entry(db.Model):
  __tablename__ = 'entries'
  id = db.Column(db.Integer, primary_key=True)
  todo_name = db.Column(db.String())
  todo_is_done = db.Column(db.Boolean())

  def __init__(self, todo_name, todo_is_done):
    self.todo_name = todo_name
    self.todo_is_done = todo_is_done

  def __repr__(self):
    return '<id {}>'.format(self.id)
  
  def serialize(self):
    return {
      'todo_name': self.todo_name,
      'todo_is_done': self.todo_is_done,
      'id': self.id
    }
