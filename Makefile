dbuild-films:
	@echo "Building films production dockerfile"
	cd ./films && docker build -f Dockerfile -t ilyadronov/cinotes-films:1.0.0 .
	docker push ilyadronov/cinotes-films:1.0.0

run:
	docker compose up -d

stop:
	docker compose stop

down:
	docker compose down

restart:
	docker compose restart

rebuild:
	docker compose down
	docker compose up -d --build
	docker image prune

logs:
	docker compose logs -f


# Django
makemigr:
	python films/manage.py makemigrations


migrate:
	python films/manage.py migrate

films-docker-shell:
	docker compose exec films sh