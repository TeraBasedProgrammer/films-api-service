build-broker:
	@echo "Building broker binary"
	cd ./broker && env GOOS=linux CGO_ENABLED=0 go build -o brokerApp ./cmd/app
	@echo "Done!"

build-auth:
	@echo "Building broker binary"
	cd ./authorization-service && env GOOS=linux CGO_ENABLED=0 go build -o authApp ./cmd/app
	@echo "Done!"

dbuild-broker: build-broker
	@echo "Building broker production dockerfile"
	cd ./broker && docker build -f broker-service.production.dockerfile -t uvarenko/cinotes-broker:test .
	docker push uvarenko/cinotes-broker:test

dbuild-auth: build-auth
	@echo "Building broker production dockerfile"
	cd ./authorization-service && docker build -f authorization-service.production.dockerfile -t uvarenko/cinotes-auth:test .
	docker push uvarenko/cinotes-auth:test

dbuild-films:
	@echo "Building films production dockerfile"
	cd ./films && docker build -f Dockerfile -t ilyadronov/cinotes-films:1.0.0 .
	docker push ilyadronov/cinotes-films:1.0.0

start:
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