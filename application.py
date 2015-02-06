from flask import Flask, jsonify
application = Flask(__name__)

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

@application.route("/")
def hello():
    return jsonify({'tasks': tasks})

if __name__ == "__main__":
    application.run(host='0.0.0.0')
