package main

import (
	"github.com/anton-uvarenko/cinema/broker-service/internal/transport/http"
	"github.com/sirupsen/logrus"
	"log"
	"net/rpc"
)

func main() {
	client, err := rpc.DialHTTP("tcp", "auth:5000")
	if err != nil {
		logrus.Error(err)
		log.Fatal(err)
	}

	c := http.NewControllers(client)
	r := http.NewRouter(c)

	handler := r.InitRoutes()

	server := http.InitHttpServer(handler)

	log.Fatal(server.ListenAndServe())

}
