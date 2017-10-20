# task-api
The HTTP REST api for the task application.  Uses python and flask with a
postgres SQL database.

# Development Environment
Use two separate terminals for development: one terminal for `git` and one
terminal for running a  
[Docker](https://store.docker.com/search?type=edition&offering=community)
container.

## Git Terminal
In the first terminal clone the repo and continue to use this terminal for
running git commands:
```
$ git clone git@github.com:chrisworman/task-api.git
$ cd task-api
$ git status              # run your git commands in this terminal
```
If a command line text editor is preferred (e.g. `vim`), use this terminal
for editing source files.

## Docker Terminal
In another terminal build the Docker image, which might take a few minutes to
complete:
```
$ cd task-api
$ ./dev.sh docker build   # build the development docker image
```
The Docker image only needs to be built once unless the `Dockerfile.dev`
file changes.

Next, run the Docker image to stand-up the development container:
```
$ ./dev.sh docker run     # run the development container from the image
```

This will bring up an interactive container with the repo directory mounted
as a volume.  Continue to use the `./dev.sh` script in the container:
```
# ./dev.sh db init        # init the sql db; this only needs to be done once
# ./dev.sh server start   # start the http server
# ./dev.sh server stop    # stop the http server
# ./dev.sh db stop        # stop the postgres sql server
# exit                    # exit the container
```

After exiting the development container, you can always run it again:
```
$ ./dev.sh docker run
# ./dev.sh db start
# ./dev.sh server start
```

## Code Changes
If you change the models in python, you need to migrate and update the
db schema in the container:
```
$ ./dev.sh db migrate     # if necessary, create a migration file for model changes
$ ./dev.sh db upgrade     # if necessary, upgrade the currently running db
```

If you install new packages, the dev script has a shortcut to `pip freeze` the
requirements:
```
$ ./dev.sh requirements freeze
```

## Development Docker Explanation
Why are we using a Docker container for development instead of relying on more
common python tools like `virtualenv`?  Part of the reason is just to try
something new, but there are other advantages.  Since the api relies on a
postgres db, standing-up a dev environment would require the developer to
install, start, and configure a postgres sql database.  The Docker container
takes care of this; it contains a configured postgres instance ready to go.
Since the Docker container is isolated from the host machine, existing
installations of postgres on the host machine do not conflict with the
requirements of the api. The Docker container also isolates the python packages
required by the api from the host machine; of course this is usually dealt with
using `virtualenv`.

Another note about the development Docker setup: the repo folder is mounted as
a volume in the container.  This allows the developer to use their favorite
text editor in the host environment, rather than relying on an editor in the
container.

# Credits
The initial version of this api was based off of a
[scotch.io tutorial](https://scotch.io/tutorials/build-a-restful-api-with-flask-the-tdd-way).
