#!/bin/bash

# This is the development management script.  Used to initialize and start
# a development environment that uses docker containers for the http server
# and the database server.

#if [ "$#" -ne 2 ]; then
#  echo "Invalid arguments"
#  echo "  usage: $ ./dev.sh [system] [command]"
#  echo "  e.g.   $ ./dev.sh server start"
#  exit 1
#fi

if [ $1 = "init" ]; then
  echo "Building http server docker image ... "
  docker build -t task-api .
  echo "Building development database docker image ... "
  docker pull postgres
elif [ $1 = "start" ]; then
    echo "Starting development environment:"
    echo "** Starting developmemnt database container ..."
    docker run --net=host --name task-api-dev-db-server -e "POSTGRES_PASSWORD=dev-password" -d postgres
    sleep 2
    docker exec -it task-api-dev-db-server psql -U postgres -c 'CREATE DATABASE tasks_api;'
    sleep 2
    echo "** Starting development api server container ..."
    docker run --net=host --name task-api-dev-http-server -e "APP_SETTINGS=development" -e "DATABASE_URL=postgresql://localhost/tasks_api?user=postgres\&password=dev-password" -d task-api
    sleep 2
    docker exec -it task-api-dev-http-server python /app/manage.py db upgrade
elif [ $1 = "clean" ]; then
  docker stop $(docker ps -a -q)
  docker rm $(docker ps -a -q)
fi

exit 0
