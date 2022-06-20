run:
	sudo python3 ./market/manage.py runserver
migrates:
	sudo python3 ./market/manage.py makemigrations && sudo python3 ./market/manage.py makemigrations back_api && sudo python3 ./market/manage.py migrate
shell:
	sudo python3 ./market/manage.py shell
tests:
	sudo python3 ./market/manage.py test back_api.tests