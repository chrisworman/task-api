# task-api
The HTTP REST api for the task application.  Uses python and flask with a
postgres SQL database.

# Development Environment
Use two separate terminals for development: one terminal for git and one
terminal for running a  
[Docker](https://store.docker.com/search?type=edition&offering=community)
container.

In the first terminal clone the repo and continue to use this terminal for
running git commands.
```
$ git clone git@github.com:chrisworman/task-api.git
$ cd task-api
```

In another terminal we'll run our development docker container:
```
$ cd task-api
$ ./dev.sh docker build # build the development docker image
$ ./dev.sh docker run   # run the development container from the image
```

This will bring up an interactive container.  Continue to use the `dev.sh`
script in the container to manage the development servers:
```
# ./dev.sh db start # start the postgres server
# ./dev.sh db init # this only needs to be done once
# ./dev.sh server start
# ./dev.sh server stop
# ./dev.sh db stop
```

## Database Model Changes
If you change the database model in python, you need to migrate and update the
db schema:
```
$ python manage.py db migrate
$ python manage.py db upgrade
```

## Code Changes
If you make code changes, esp. new imports, consider running:
```
$ pip freeze > requirements.txt
```

# Credits
The initial version of this api was based off of a
(scotch.io tutorial)[https://scotch.io/tutorials/build-a-restful-api-with-flask-the-tdd-way].
