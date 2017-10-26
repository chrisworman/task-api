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
    docker run -p 5432:5432 --name task-api-dev-db-server -e "POSTGRES_PASSWORD=dev_password" -d postgres
    sleep 2
    dbServerIPAddress="$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' task-api-dev-db-server)"
    docker exec -it task-api-dev-db-server psql -U postgres -c "CREATE DATABASE tasks_api;"
    echo "** Starting development api server container ..."
    docker run -it -p 80:80 --name task-api-dev-http-server -e "APP_SETTINGS=development" -e "DATABASE_URL=postgresql://$dbServerIPAddress/tasks_api?user=postgres&password=dev_password" -d task-api
    sleep 2
    docker exec -it task-api-dev-http-server python /app/manage.py db upgrade
elif [ $1 = "clean" ]; then
  docker stop $(docker ps -a -q)
  docker rm $(docker ps -a -q)
fi

exit 0
