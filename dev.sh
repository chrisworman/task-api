#!/bin/bash

if [ $1 = "docker" ]; then
  if [ $2 = "build" ]; then
    docker build -f Dockerfile.dev -t task-api-dev .
  elif [ $2 = "run" ]; then
    docker run -v `pwd`:/usr/src/app:ro -i -t -p 5000:5000 task-api-dev
  fi
elif [ $1 = "db" ]; then
  if [ $2 = "start" ]; then
   service postgresql start
  elif [ $2 = "init" ]; then
    su -c 'createdb tasks_api' - postgres
    su -c 'psql -U postgres -d tasks_api -a -f /usr/src/app/create-dev-user.sql' - postgres
    python manage.py db upgrade
  elif [ $2 = "stop" ]; then
    service postgresql stop
  fi
elif [ $1 = "server" ]; then
    if [ $2 = "start" ]; then
      flask run &
    elif [ $2 = "stop" ]; then
      pkill flask
    fi
fi
