from application import db
from sqlalchemy.dialects.postgresql import JSON

class Entry(db.Model):
  __tablename__ = 'entries'

  id = db.Column(db.Integer, primary_key=True)
  url = db.Column(db.String())
  entries_all = db.Column(JSON)


  def __initi__(self, url, entries_all):
    self.url = url
    self.entries_all = entries_all

  def __repr__(self):
    return '<id {}>'.format(self.id)
