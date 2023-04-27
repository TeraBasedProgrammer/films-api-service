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

start:
	docker compose up -d

stop:
	docker compose stop