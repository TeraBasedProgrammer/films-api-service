package main

import (
	"github.com/anton-uvarenko/cinema/broker-service/internal/transport/http"
	rpc2 "github.com/anton-uvarenko/cinema/broker-service/internal/transport/rpc"
	"log"
	"net/rpc"
)

func main() {
	client := make(chan *rpc.Client)

	go rpc2.ConnectServer(client, "auth", "5000")

	c := http.NewControllers(<-client)
	r := http.NewRouter(c)

	handler := r.InitRoutes()

	server := http.InitHttpServer(handler)

	log.Fatal(server.ListenAndServe())

}
