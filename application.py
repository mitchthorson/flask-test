from flask import Flask, jsonify, request, abort, make_response
import os
from datetime import timedelta
from functools import update_wrapper
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

def crossdomain(origin=None, methods=None, headers=None,
    max_age=21600, attach_to_all=True,
    automatic_options=True):
    
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = application.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = application.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

@application.errorhandler(404)
@crossdomain(origin='*')
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@application.route("/", methods=['GET'])
@crossdomain(origin='*')
def hello():
    return jsonify({'tasks': tasks})

@application.route('/todos', methods=['GET'])
@crossdomain(origin='*')
def get_all():
    all_records = Entry.query.all()
    record_list = []
    for record in all_records:
        record_obj = record.serialize()
        record_list.append(record_obj)
    return jsonify(({'todos': record_list}));

@application.route("/todos", methods=['POST', 'OPTIONS'])
@crossdomain(origin='*', headers='Content-Type')
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
        return jsonify(todo.serialize())
    except NameError as e:
        print e
        errors.append("Unable to add items to database")
        return make_response(jsonify({'errors': errors}), 400)

@application.route("/todos/<int:todo_id>", methods=['GET'])
@crossdomain(origin='*')
def get_todo(todo_id):
    todo_record = Entry.query.get(todo_id)
    if todo_record is not None:
        return jsonify(todo_record.serialize()), 200
    else:
        abort(404)


@application.route("/todos/<int:todo_id>", methods=['PUT', 'OPTIONS'])
@crossdomain(origin='*')
def update_todo(todo_id):
    if not request.json or not 'todo_name' in request.json or not 'todo_is_done' in request.json:
      abort(400)
    todo_record = Entry.query.get(todo_id)
    if todo_record is not None:
        todo_name = request.json['todo_name']
        todo_is_done = request.json['todo_is_done']
        todo_record.todo_name = todo_name
        todo_record.todo_is_done = todo_is_done
        db.session.commit()
        return jsonify(todo_record.serialize()), 200
    else:
        abort(404)


@application.route('/todos/<int:todo_id>', methods=['DELETE', 'OPTIONS'])
@crossdomain(origin='*')
def delete_todo(todo_id):
  todo_record = Entry.query.get(todo_id)
  if todo_record is None:
    return jsonify({'error': 'item not found in database'}), 400
  else:
    try:
      db.session.delete(todo_record)
      db.session.commit()
      return jsonify({'deleted': todo_record.serialize()}), 200
    except:
      return jsonify({'error': 'Unable to delete items in database'}), 400
    return


if __name__ == "__main__":
    application.run(host='0.0.0.0')




