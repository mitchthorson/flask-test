from flask import Flask, jsonify, request, abort, make_response
import os
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

@application.route("/add", methods=['POST'])
def create_task():
    print request.args.get('key')
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    resp = make_response(jsonify({'task': task}), 201)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

if __name__ == "__main__":
    application.run(host='0.0.0.0')




