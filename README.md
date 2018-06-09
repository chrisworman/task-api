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
the `log` command:
```
$ ./dev.sh http log
$ ./dev.sh db log
```

The source code for the app is mounted in the http container.  If you want
to apply code changes, you need to restart the http server:
```
$ ./dev.sh http restart
```

If want to execute a command in a container, for example to install python
packages with `pip`, use the `attach` command to start a bash shell in the
desired container:
```
$ ./dev.sh http attach
$ ./dev.sh db attach
```
Type `exit` to detach from the container.

Rather than attaching to a container and running commands, the dev script
also has shortcuts to common commands:
```
$ ./dev.sh http freeze       # runs "pip freeze > requirements.txt" in the http container
$ ./dev.sh db migrate        # runs a db migrate and upgrade
```

When you are done working with the api, you can stop and remove the containers
using the `stop` command.  You can start the api again with the `start`
command.
```
$ ./dev.sh stop
$ ./dev.sh start
```

## Development Docker Explanation
Why are we using a docker container for development instead of relying on more
common python tools like `virtualenv`?  Part of the reason is just to try
something new, but there are other advantages.  

* Since the api relies on a postgres db, standing-up a dev environment would
require the developer to install, start, and configure a postgres sql database.  
Since the docker container is isolated from the host machine, existing
installations of postgres on the host machine do not conflict with the
requirements of the api.

* The docker container also isolates the python packages required by the api
from the host machine; of course this is usually dealt with using `virtualenv`.

* The production deployment of the api uses the same docker image as the
development environment, which helps with continuous deployment.

Another note about the development docker setup: the repo folder is mounted as
a volume in the container.  This allows the developer to use their favorite
text editor in the host environment, rather than relying on an editor in the
container.

# Production Deployment Using AWS Elastic Beanstalk

* http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/docker-singlecontainer-deploy.html

Install the Elastic Beanstalk Command Line Interface (EB CLI)
(http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3-install.html):
```
pip install awsebcli --upgrade --user
```

Add the following to your `~/.bash_profile`:
```
export PATH=~/Library/Python/2.7/bin:$PATH
```

Configure AWS security groups for EB & RDS:
http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/AWSHowTo.RDS.html

# Credits
The initial version of this api was based off of a
[scotch.io tutorial](https://scotch.io/tutorials/build-a-restful-api-with-flask-the-tdd-way).
