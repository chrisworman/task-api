#!/bin/bash

# This is the deployment management script.  Uses a docker container to
# upgrade or downgrade remote dbs.
# TODO: add ebs deployment commands

function show_usage_and_exit {
  echo "usage: ./deploy.sh [command]"
  echo ""
  echo "   commands:"
  echo ""
  echo "      db upgrade [APP_SETTINGS] [DATABASE_URL]"
  exit 1
}

function db_upgrade {
  echo "> Upgrading db  ..."
  docker run -itd -v `pwd`:/app -p 81:80 --name task-api-deploy -e "APP_SETTINGS=$1" -e "DATABASE_URL=$2" task-api &&
  docker exec -it task-api-deploy python /app/manage.py db upgrade &&
  docker stop task-api-deploy && docker rm task-api-deploy
  return 0
}

# At least one argument required
if [ "$#" -eq 0 ]; then
  show_usage_and_exit
fi

if [ $1 = "db" ]; then

  if [ "$#" -ne 4 ]; then
    show_usage_and_exit
  fi

  if [ $2 = "upgrade" ]; then
    db_upgrade $3 $4
  else
    show_usage_and_exit
  fi

else
  show_usage_and_exit
fi

exit 0
