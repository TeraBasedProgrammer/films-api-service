

build-broker:
	@echo "Building broker binary"
	cd ./broker && env GOOS=linux CGO_ENABLED=0 go build -o brokerApp ./cmd/app
	@echo "Done!"

build-auth:
	@echo "Building broker binary"
	cd ./authorization-service && env GOOS=linux CGO_ENABLED=0 go build -o authApp ./cmd/app
	@echo "Done!"

#dbuild-broker:
#	@echo "Building broker production dockerfile"
#	cd ./broker && docker build