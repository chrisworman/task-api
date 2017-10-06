# task-api
The api for the task application.  Based off of https://scotch.io/tutorials/build-a-restful-api-with-flask-the-tdd-way.

# Setup

If you don't have postgres:
```
$ brew install postgresql
$ initdb /usr/local/var/postgres -E utf8
$ pg_ctl -D /usr/local/var/postgres -l logfile start
```

Ensure you have `virtualenv`. Then:

```
$ git clone git@github.com:chrisworman/task-api.git
$ cd task-api
$ virtualenv env
$ source env/bin/activate
$ env/bin/pip install -r requirements.txt
$ createdb tasks_api
$ python manage.py db upgrade
$ flask run
$ # ... api server should be listening now! ...
$ deactivate
```

TODO: talk about `.env` or include boiler plate?
