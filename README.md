# task-api
The HTTP REST api for the task application.  Uses python and flask with with a
postgres SQL database.

# Development Setup
The api requires `python` (with supporting cast) and `postgres`.  A production
setup will vary based upon needs, but will be similar to the Development setup.

## Prerequisites
If you don't already have `postgres`, install and initialize:
```
$ brew install postgresql
$ initdb /usr/local/var/postgres -E utf8
```

Start postgres if it is not already running:
```
$ pg_ctl -D /usr/local/var/postgres -l logfile start
```

You'll need the basic `python` tools, i.e. `pip` and `virtualenv`:

## Cloning and Starting the API
```
$ git clone git@github.com:chrisworman/task-api.git
$ cd task-api
$ virtualenv env
$ source env/bin/activate
(env) $ pip install -r requirements.txt
(env) $ createdb tasks_api
(env) $ python manage.py db upgrade
(env) $ flask run
(env) $ # api should be listening now ... CTRL+C to stop
$ deactivate
```

TODO: talk about `.env` or include boiler plate?

# Credits
This api is loosely based off of https://scotch.io/tutorials/build-a-restful-api-with-flask-the-tdd-way.
