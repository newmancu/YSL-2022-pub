#!/bin/bash

echo "CREATE SECRET_KEY"
python ./market/create_secret.py

echo "Creating migrations"

while ! python ./market/manage.py makemigrations 2>&1; do
  echo "python manage.py makemigrations"
  sleep 3
done

echo "Migrate the Database at startup of project"

while ! python ./market/manage.py migrate  2>&1; do
   echo "Migration is in progress status"
   sleep 3
done


echo "Django docker is fully configured successfully."


exec "$@"