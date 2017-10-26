# task-api
The HTTP REST api for the task application.  Uses python and flask with a
postgres SQL database.  Docker is used to containerize the app in a way
that works in all environments, including development and production.

# Development Environment
The development environment has two requirements:
[git](https://git-scm.com/downloads) and
[docker](https://store.docker.com/search?type=edition&offering=community).
Once you have `docker` running, clone the repo:
```
$ git clone git@github.com:chrisworman/task-api.git
$ cd task-api
```

The development environment is managed by the `dev.sh` script.  First build
the development docker containers:
```
$ ./dev.sh build
```

Use the `start` command to start the development environment:
```
$ ./dev.sh start
```

This will bring up two containers, one running the db server and one
running the http server.  You can inspect activity in the containers using
the `logs` command:
```
$ ./dev.sh logs http
$ ./dev.sh logs db
```

The source code for the app is mounted in the http container.  If you want
to apply code changes, you need to restart the http server:
```
$ ./dev.sh restart http
```

If you change the data models in python, you need to generate migration scripts
and upgrade the database:
```
$ ./dev.sh migrate
```

If you install new packages, the `./dev.sh` script has a shortcut to run
`pip freeze > requirements.txt`:
```
$ ./dev.sh freeze
```

When you are done working with the api, you can stop and remove the containers
using the `stop` command.  You can then start the api again with the `start`
command.
```
$ ./dev.sh stop
```

## Development Docker Explanation
Why are we using a docker container for development instead of relying on more
common python tools like `virtualenv`?  Part of the reason is just to try
something new, but there are other advantages.  Since the api relies on a
postgres db, standing-up a dev environment would require the developer to
install, start, and configure a postgres sql database.  The docker container
takes care of this; it contains a configured postgres instance ready to go.
Since the docker container is isolated from the host machine, existing
installations of postgres on the host machine do not conflict with the
requirements of the api. The docker container also isolates the python packages
required by the api from the host machine; of course this is usually dealt with
using `virtualenv`.

Another note about the development docker setup: the repo folder is mounted as
a volume in the container.  This allows the developer to use their favorite
text editor in the host environment, rather than relying on an editor in the
container.

# Credits
The initial version of this api was based off of a
[scotch.io tutorial](https://scotch.io/tutorials/build-a-restful-api-with-flask-the-tdd-way).
