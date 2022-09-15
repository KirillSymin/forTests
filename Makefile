build:
	sudo chmod -R 775 ../
	cp local_settings.env ./django/YandexDisk/application/
	sudo docker-compose build

up:build
	sudo docker-compose up -d
	sudo docker-compose exec django python3 ./manage.py migrate

migrate:up
	sudo docker-compose exec django python3 ./manage.py migrate

createsuperuser:migrate
	sudo docker-compose exec django python3 ./manage.py createsuperuser

stop:
	sudo docker-compose stop

clear:
	sudo docker-compose down