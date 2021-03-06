#!env/bin/python
import os
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort, Flask
from flask_cors import CORS
from config import config_from_app_settings
import pprint
import json

db = SQLAlchemy()

def create_app(app_settings):

    from models import Task
    from models import List

    app = Flask(__name__)
    app.config.from_object(config_from_app_settings(app_settings))
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.url_map.strict_slashes = False

    cors = CORS(app)
    db.init_app(app)

    @app.route("/")
    def hello():
        return "task-api from eb cli"

    # /lists

    @app.route('/lists/', methods=['POST'])
    def lists_post():
        name = request.get_json()['name']
        if name:
            list = List(name=name)
            list.save()
            response = jsonify(list_api_model(list))
            response.status_code = 201
            return response
        else:
            return ('Bad request: name is required', 400)

    @app.route('/lists/', methods=['GET'])
    def lists_get():
        lists = List.get_all()
        results = []
        for list in lists:
            api_model = list_api_model(list)
            results.append(api_model)
        response = jsonify(results)
        response.status_code = 200
        return response

    @app.route('/lists/<int:list_id>', methods=['DELETE'])
    def lists_delete(list_id):
        list = List.get_by_id(list_id=list_id)
        if list:
            list.delete()
            return ('', 204)
        else:
            return ('List not found', 404)

    @app.route('/lists/<int:list_id>', methods=['GET'])
    def lists_get_by_id(list_id):
        list = List.get_by_id(list_id=list_id)
        if list:
            response = jsonify(list_api_model(list))
            response.status_code = 200
            return response
        else:
            return ('List not found', 404)

    @app.route('/lists/<int:list_id>', methods=['PUT'])
    def lists_put(list_id):
        db_list = List.get_by_id(list_id)
        if db_list:
            db_list.name = request.get_json()['name']
            db_list.save()
            return ('', 204)
        else:
            return ('List not found', 404)

    # Convert a "list" DB model to it's equivalent api model
    def list_api_model(list_db_model):
        api_model = {
            'id': list_db_model.id,
            'name': list_db_model.name,
            'date_created': list_db_model.date_created,
            'date_modified': list_db_model.date_modified
        }
        return api_model

    # /tasks

    @app.route('/tasks/', methods=['POST'])
    def tasks_post():
        list_id = int(request.get_json()['list_id'])
        text = request.get_json()['text']
        marked = request.get_json()['marked']
        if text and list_id > 0:
            task = Task(list_id=list_id, text=text, marked=marked)
            task.save()
            response = jsonify(task_api_model(task))
            response.status_code = 201
            return response
        else:
            return ('Missing parameter: text and list_id required.', 400)

    @app.route('/tasks/', methods=['GET'])
    def tasks_get():
        list_id = int(request.args.get('list_id'))
        marked = string_is_true(request.args.get('marked'))
        tasks = Task.get_by_list_id(list_id)
        tasks = [task for task in tasks if task.marked == marked]
        results = []
        for task in tasks:
            api_model = task_api_model(task)
            results.append(api_model)
        response = jsonify(results)
        response.status_code = 200
        return response

    @app.route('/tasks/<int:task_id>', methods=['PUT'])
    def tasks_put(task_id):
        db_task = Task.get_by_id(task_id)
        if db_task:
            db_task.text = request.get_json()['text']
            db_task.list_id = request.get_json()['list_id']
            db_task.marked = request.get_json()['marked']
            db_task.save()
            return ('', 204)
        else:
            return ('Task not found', 404)

    @app.route('/tasks/<int:task_id>', methods=['DELETE'])
    def tasks_delete(task_id):
        task = Task.get_by_id(task_id=task_id)
        if task:
            task.delete()
            return ('', 204)
        else:
            return ('Task not found', 404)

    # Is the specified string case-insensitive "true"?
    def string_is_true(targetString):
        if (targetString is not None) and (targetString.lower() == "true"):
            return True
        else:
            return False

    # Convert a "task" DB model to it's equivalent api model
    def task_api_model(task_db_model):
        api_model = {
            'id': task_db_model.id,
            'list_id': task_db_model.list_id,
            'text': task_db_model.text,
            'marked': task_db_model.marked,
            'date_created': task_db_model.date_created,
            'date_modified': task_db_model.date_modified
        }
        return api_model

    return app

app_settings = os.getenv('APP_SETTINGS')
app = create_app(app_settings)

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)
