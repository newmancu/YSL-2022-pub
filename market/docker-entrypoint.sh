#!/bin/bash

echo "CREATE SECRET_KEY"
python ./market/create_secret.py

echo "Creating migrations"

while ! python ./market/manage.py makemigrations 2>&1; do
  echo "python manage.py makemigrations"
  sleep 1
done

while ! python ./market/manage.py makemigrations back_api 2>&1; do
  echo "python manage.py makemigrations"
  sleep 1
done

echo "Migrate the Database at startup of project"

while ! python ./market/manage.py migrate  2>&1; do
   echo "Migration is in progress status"
   sleep 1
done

while ! python ./market/manage.py migrate back_api 2>&1; do
   echo "Migration is in progress status"
   sleep 1
done


echo "Django docker is fully configured successfully."


exec "$@"