#!env/bin/python
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort
from flask_cors import CORS
from instance.config import app_config
import pprint
import json

# initialize sql-alchemy
db = SQLAlchemy()

def create_app(config_name):
    from app.models import Task
    from app.models import List

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    cors = CORS(app)
    db.init_app(app)

    # routing
    app.url_map.strict_slashes = False

    # /lists

    @app.route('/lists/', methods=['POST'])
    def lists_post():
        name = request.data.get('name', '')
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
            response = jsonify({
                'id': list.id,
                'name': list.name,
                'date_created': list.date_created,
                'date_modified': list.date_modified
            })
            response.status_code = 200
            return response
        else:
            return ('List not found', 404)

    @app.route('/lists/<int:list_id>', methods=['PUT'])
    def lists_put(list_id):
        db_list = List.get_by_id(list_id)
        if db_list:
            db_list.name = request.data.get('name')
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
        list_id = int(request.data.get('list_id'))
        text = request.data.get('text')
        marked = request.data.get('marked')
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
        tasks = Task.get_by_list_id(list_id)
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
            db_task.text = request.data.get('text')
            db_task.list_id = request.data.get('list_id')
            db_task.marked = request.data.get('marked')
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
