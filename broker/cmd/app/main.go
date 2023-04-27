package main

import (
	"github.com/anton-uvarenko/cinema/broker-service/internal/transport/grpc"
	"github.com/anton-uvarenko/cinema/broker-service/internal/transport/http"
	"github.com/sirupsen/logrus"
	"log"
)

func main() {
	logrus.Info("connecting to auth")
	clients := grpc.ConnectAuthServer()

	c := http.NewControllers(clients)
	r := http.NewRouter(c)

	handler := r.InitRoutes()

	server := http.InitHttpServer(handler)

	log.Fatal(server.ListenAndServe())
}
