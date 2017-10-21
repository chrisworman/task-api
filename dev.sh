#!/bin/bash

if [ "$#" -ne 2 ]; then
  echo "Invalid arguments"
  echo "  usage: $ ./dev.sh [system] [command]"
  echo "  e.g.   $ ./dev.sh server start"
  exit 1
fi

if [ $1 = "docker" ]; then
  if [ $2 = "build" ]; then
    docker build -f Dockerfile.dev -t task-api-dev .
  elif [ $2 = "run" ]; then
    docker run -v `pwd`:/usr/src/app -i -t -p 5000:5000 task-api-dev
  fi
elif [ $1 = "db" ]; then
  if [ $2 = "start" ]; then
   service postgresql start
  elif [ $2 = "init" ]; then
    service postgresql start
    su -c 'createdb tasks_api' - postgres
    su -c 'psql -U postgres -d tasks_api -a -f /usr/src/app/create-dev-user.sql' - postgres
    python /usr/src/app/manage.py db upgrade
  elif [ $2 = "migrate" ]; then
    python /usr/src/app/manage.py db migrate
  elif [ $2 = "upgrade" ]; then
    python /usr/src/app/manage.py db upgrade
  elif [ $2 = "stop" ]; then
    service postgresql stop
  fi
elif [ $1 = "server" ]; then
    if [ $2 = "start" ]; then
      flask run &
    elif [ $2 = "stop" ]; then
      pkill flask
    fi
elif [ $1 = "requirements" ]; then
    if [ $2 = "freeze" ]; then
      pip freeze > requirements.txt
    elif [ $2 = "install" ]; then
      pip install --no-cache-dir -r requirements.txt
    fi
fi
