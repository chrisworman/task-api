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

    # /tasks

    @app.route('/tasks/', methods=['POST'])
    def tasks_post():
        list_id = int(request.data.get('list_id'))
        text = request.data.get('text')
        if text and list_id > 0:
            task = Task(list_id=list_id,text=text)
            task.save()
            response = jsonify({
                'id': task.id,
                'list_id': task.list_id,
                'text': task.text,
                'date_created': task.date_created,
                'date_modified': task.date_modified
            })
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
            obj = {
                'id': task.id,
                'list_id': task.list_id,
                'text': task.text,
                'date_created': task.date_created,
                'date_modified': task.date_modified
            }
            results.append(obj)
        response = jsonify(results)
        response.status_code = 200
        return response

    @app.route('/tasks/<int:task_id>', methods=['PUT'])
    def tasks_put(task_id):
        db_task = Task.get_by_id(task_id)
        if db_task:
            db_task.text = request.data.get('text')
            db_task.list_id = request.data.get('list_id')
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

    # /lists

    @app.route('/lists/', methods=['POST'])
    def lists_post():
        name = request.data.get('name', '')
        if name:
            list = List(name=name)
            list.save()
            response = jsonify({
                'id': list.id,
                'name': list.name,
                'date_created': list.date_created,
                'date_modified': list.date_modified
            })
            response.status_code = 201
            return response
        else:
            return ('Bad request: name is required', 400)

    @app.route('/lists/', methods=['GET'])
    def lists_get():
        lists = List.get_all()
        results = []
        for l in lists:
            obj = {
                'id': l.id,
                'name': l.name,
                'date_created': l.date_created,
                'date_modified': l.date_modified
            }
            results.append(obj)
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

    return app
