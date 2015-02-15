from flask import Flask, jsonify, request, abort, make_response
import os
import sys
from flask.ext.sqlalchemy import SQLAlchemy

application = Flask(__name__)
application.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(application)

from models import *



tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': True
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': True
    }
]

@application.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@application.route("/", methods=['GET'])
def hello():
    print request.headers['Host']
    resp = make_response(jsonify({'tasks': tasks}))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    # print resp.headers
    return resp

@application.route('/todos', methods=['GET'])
def get_all():
    all_records = Entry.query.all()
    record_list = []
    for record in all_records:
      record_obj = record.serialize()
      record_list.append(record_obj)
    resp = make_response(jsonify({'todos': record_list}), 200)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@application.route("/add", methods=['POST'])
def create_task():
    if not request.json or not 'todo_name' in request.json:
        abort(400)
    errors = []
    todo_name = request.json['todo_name']

    try: 
      todo = Entry(todo_name,False)
      db.session.add(todo)
      db.session.commit()
      print todo
      resp = make_response(jsonify(todo.serialize()), 201)
    except NameError as e:
      print e
      errors.append("Unable to add items to database")
      resp = make_response(jsonify({'errors': errors}), 400)

    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

if __name__ == "__main__":
    application.run(host='0.0.0.0')




