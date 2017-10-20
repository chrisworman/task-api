# task-api
The HTTP REST api for the task application.  Uses python and flask with a
postgres SQL database.

# Development Environment
Use two separate terminals for development: one terminal for git and one
terminal for running a  
[Docker](https://store.docker.com/search?type=edition&offering=community)
container.

In the first terminal clone the repo and continue to use this terminal for
running git commands, freezing pip requirements, and other changes to the repo
directory.
```
$ git clone git@github.com:chrisworman/task-api.git
$ cd task-api
```

In another terminal we'll create our development docker image, which will
take a few minutes to complete:
```
$ cd task-api
$ ./dev.sh docker build   # build the development docker image
```
We rarely need to run `docker build`; situations that require
a build include changes to `requirements.txt` or `Dockerfile.dev`.

Next, we run our image to create our development container, which will mount
the repo directory in read-only mode:
```
$ ./dev.sh docker run     # run the development container from the image
```

This will bring up an interactive container.  Continue to use the `dev.sh`
script in the container to manage the development servers:
```
# ./dev.sh db start       # start the postgres sql server
# ./dev.sh db init        # init the sql ddb; this only needs to be done once
# ./dev.sh server start   # start the http server
# ./dev.sh server stop    # stop the http server
# ./dev.sh db stop        # stop the postgres sql server
# exit                    # exit the container
```

After you've left the development container, you can always run it again:
```
$ ./dev.sh docker run
# ./dev.sh db start
# ./dev.sh server start
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
[scotch.io tutorial](https://scotch.io/tutorials/build-a-restful-api-with-flask-the-tdd-way).
