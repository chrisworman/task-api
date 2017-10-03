#!env/bin/python
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort

# local import
from instance.config import app_config

# initialize sql-alchemy
db = SQLAlchemy()

def create_app(config_name):
    from app.models import Task

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/tasks/', methods=['POST', 'GET'])
    def tasks():
        if request.method == "POST":
            list_id = int(request.data.get('list_id', 0))
            text = str(request.data.get('text', ''))
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
            # GET
            tasks = Task.get_all()
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

    return app
