#!/bin/bash

# This is the development management script.  Used to build, start, and
# stop a development environment that uses docker containers for the http server
# and the database server.

if [ $1 = "build" ]; then

  echo "> Building http server docker container image ... "
  docker build -t task-api .

  echo "> Pulling development database docker container image ... "
  docker pull postgres

elif [ $1 = "start" ]; then

  echo "> Starting database container ..."
  docker run -p 5432:5432 --name task-api-dev-db-server -e "POSTGRES_PASSWORD=dev_password" -d postgres
  sleep 3
  dbServerIPAddress="$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' task-api-dev-db-server)"
  docker exec -it task-api-dev-db-server psql -U postgres -c "CREATE DATABASE tasks_api;"

  echo "> Starting http server container ..."
  docker run -itd -v `pwd`:/app -p 80:80 --name task-api-dev-http-server -e "APP_SETTINGS=development" -e "DATABASE_URL=postgresql://$dbServerIPAddress/tasks_api?user=postgres&password=dev_password" task-api
  docker exec -it task-api-dev-http-server python /app/manage.py db upgrade

  echo "task-api should be listening on http://localhost:80/"

elif [ $1 = "stop" ]; then

  docker stop task-api-dev-db-server task-api-dev-http-server
  docker rm task-api-dev-db-server task-api-dev-http-server

elif [ $1 = "db" ]; then

  if [ $2 = "logs" ]; then
    docker logs task-api-dev-db-server
  elif [ $2 = "migrate" ]; then
    docker exec -it task-api-dev-http-server python /app/manage.py db migrate
    docker exec -it task-api-dev-http-server python /app/manage.py db upgrade
  elif [ $2 = "attach" ]; then
    docker exec -it task-api-dev-db-server bash
  fi

elif [ $1 = "http" ]; then

  if [ $2 = "restart" ]; then
    echo "> Restarting http server ..."
    docker stop task-api-dev-http-server
    docker rm task-api-dev-http-server
    docker run -itd -v `pwd`:/app -p 80:80 --name task-api-dev-http-server -e "APP_SETTINGS=development" -e "DATABASE_URL=postgresql://$dbServerIPAddress/tasks_api?user=postgres&password=dev_password" task-api
    echo "task-api should be listening on http://localhost:80/"
  elif [ $2 = "logs" ]; then
    docker logs task-api-dev-http-server
  elif [ $2 = "freeze" ]; then
    docker exec -it task-api-dev-http-server pip freeze > requirements.txt
  elif [ $2 = "attach" ]; then
    docker exec -it task-api-dev-http-server bash
  fi

else

  echo "Unrecognized command: $1"
  echo "usage: ./dev.sh [ build | start | stop | http [logs|restart|freeze|attach] | db [logs|migrate|attach]"
  exit 1

fi

exit 0
