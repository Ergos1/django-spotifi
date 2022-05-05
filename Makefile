container_name = spotifi-app
db_container_name = spotifi-app-db
cron_container_name = spotifi-app-cron
db_name = todo
db_user = yergeldi

enter-api:
	docker exec -it $(container_name) bash -c 'HOME=/bash/home bash'

enter-db:
	docker exec -it $(db_container_name) psql -U $(db_user) $(db_name)

enter-cron:
	docker exec -it $(cron_container_name) bash -c 'HOME=/bash/home bash'

create-admin:
	docker exec -it $(container_name) python manage.py createsuperuser

migrate-create-and-run:
	docker exec -it $(container_name) python manage.py makemigrations $(name) 
	docker exec -it $(container_name) python manage.py migrate $(name) 

restart:
	docker-compose down
	sudo docker-compose up -d --build

cron-add:
	docker exec -it $(container_name) python manage.py crontab add

cron-rm:
	docker exec -it $(container_name) python manage.py crontab remove

cron-show:
	docker exec -it $(container_name) python manage.py crontab show

show-logs:
	docker-compose logs -f --tail 100

# # clear-logs:
# 	echo "" > $(docker inspect --format='{{.LogPath}}' spotifi-app-db)