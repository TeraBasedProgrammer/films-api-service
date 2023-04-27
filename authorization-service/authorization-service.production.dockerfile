FROM alpine:latest
WORKDIR /app
COPY authApp ./
CMD ./authApp