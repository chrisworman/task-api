#!/bin/bash

# This is the development management script.  Used to build, start, and
# stop a development environment that uses docker containers for the http server
# and the database server.

function show_usage_and_exit {
  echo "usage: ./dev.sh [command]"
  echo ""
  echo "   commands:"
  echo ""
  echo "      build        - build the dev containers"
  echo "      start        - start the dev containers"
  echo "      stop         - stop the dev containers"
  echo ""
  echo "      http log     - view the log from the dev http container"
  echo "      http restart - restart the dev http container"
  echo "      http freeze  - run 'pip freeze > requirements.txt"
  echo "      http attach  - attach a bash shell to the http container"
  echo ""
  echo "      db log       - view the log from the dev http container"
  echo "      db migrate   - if necessary, create a db migration script"
  echo "      db upgrade   - if necessary, upgrade the db using migrations"
  echo "      db attach    - attach a bash shell to the db container"
  exit 1
}

# At least one argument required
if [ "$#" -eq 0 ]; then
  show_usage_and_exit
fi

function build_docker_images {
  echo "> Building http server docker image ... "
  docker build -t task-api . &&
  echo "> Pulling development database docker image ... " &&
  docker pull postgres
  return 0
}

function start_db_container {
  echo "> Starting database container ..."
  docker run -p 5432:5432 --name task-api-dev-db -e "POSTGRES_PASSWORD=dev_password" -d postgres &&
  sleep 5 &&
  docker exec -it task-api-dev-db psql -U postgres -c "CREATE DATABASE tasks_api;"
  echo "> DB listening on port 5432"
  return 0
}

function set_http_port {
  HTTP_PORT="8081" # default http api port
  if [ "$#" -gt 0 ]; then
    HTTP_PORT="$1"
  fi
}

function start_http_container {
  echo "> Starting http server container ..."
  set_http_port $1
  DB_SERVER_IP_ADDRESS="$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' task-api-dev-db)"
  DB_URL="postgresql://$DB_SERVER_IP_ADDRESS/tasks_api?user=postgres&password=dev_password"
  docker run -itd -v `pwd`:/app -p "$HTTP_PORT":80 --name task-api-dev-http -e "APP_SETTINGS=development" -e "DATABASE_URL=$DB_URL" task-api &&
  docker exec -it task-api-dev-http python /app/manage.py db upgrade &&
  printf "HTTP API listening on port %s\n" "$HTTP_PORT"
  return 0
}

function stop_and_remove_http_container {
  echo "> Stopping and removing http container ..."
  docker stop task-api-dev-http && docker rm task-api-dev-http
  return 0
}

function stop_and_remove_db_container {
  echo "> Stopping and removing db container ..."
  docker stop task-api-dev-db && docker rm task-api-dev-db
  return 0
}

function restart_http_container {
  echo "> Restarting http server container ..."
  stop_and_remove_http_container && start_http_container $1
  return 0
}

function stop_and_remove_containers {
  stop_and_remove_http_container && stop_and_remove_db_container
  return 0
}

function migrate_db {
  echo "> Migrating ..."
  docker exec -it task-api-dev-http python /app/manage.py db migrate
  return 0
}

function upgrade_db {
  echo "> Upgrading db ..."
  docker exec -it task-api-dev-http python /app/manage.py db upgrade
  return 0
}

function remove_images {
  stop_and_remove_containers &&
  echo "> Removing http server image ..." &&
  docker rmi task-api
  return 0
}

if [ $1 = "build" ]; then
  build_docker_images
elif [ $1 = "start" ]; then
   start_db_container && start_http_container $2
elif [ $1 = "stop" ]; then
  stop_and_remove_containers
elif [ $1 = "clean" ];  then
  remove_images
elif [ $1 = "db" ]; then

  if [ "$#" -ne 2 ]; then
    show_usage_and_exit
  fi

  if [ $2 = "log" ]; then
    docker logs task-api-dev-db
  elif [ $2 = "migrate" ]; then
    migrate_db
  elif [ $2 = "upgrade" ]; then
    upgrade_db
  elif [ $2 = "attach" ]; then
    docker exec -it task-api-dev-db bash
  else
    show_usage_and_exit
  fi

elif [ $1 = "http" ]; then

  if [ "$#" -ne 2 ]; then
    show_usage_and_exit
  fi

  if [ $2 = "restart" ]; then
    restart_http_container $3
  elif [ $2 = "log" ]; then
    docker logs task-api-dev-http
  elif [ $2 = "freeze" ]; then
    docker exec -it task-api-dev-http pip freeze > requirements.txt
  elif [ $2 = "attach" ]; then
    docker exec -it task-api-dev-http bash
  else
    show_usage_and_exit
  fi

else
  show_usage_and_exit
fi

exit 0
