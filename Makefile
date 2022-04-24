container_name = spotifi-app
db_container_name = spotifi-app-db
db_name = todo
db_user = yergeldi

enter-api:
	docker exec -it $(container_name) bash -c 'HOME=/bash/home bash'

enter-db:
	docker exec -it $(db_container_name) psql -U $(db_user) $(db_name)

create-admin:
	docker exec -it $(container_name) python manage.py createsuperuser

migrate-create:
	docker exec -it $(container_name) python manage.py makemigrations $(name) 
	docker exec -it $(container_name) python manage.py migrate $(name) 


migrate:
	docker exec -it $(container_name) python manage.py migrate 

restart:
	docker-compose down
	sudo docker-compose up -d --build

all:
	docker exec -it $(db_container_name) psql -U $(db_user) $(db_name) | echo "select * from main_task;"
