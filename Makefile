build-broker:
	@echo "Building broker binary"
	cd ./broker &&
	go build -o brokerApp ./cmd/app/main.go
	@echo "Done!"