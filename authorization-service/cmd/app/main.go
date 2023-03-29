package main

import (
	"github.com/anton-uvarenko/cinema/authorization-service/internal/core/database"
	"github.com/anton-uvarenko/cinema/authorization-service/internal/core/repo"
	"github.com/anton-uvarenko/cinema/authorization-service/internal/services"
	"github.com/anton-uvarenko/cinema/authorization-service/internal/transport/rpc"
	"github.com/sirupsen/logrus"
	"google.golang.org/grpc"
	"log"
	"net"
)

func main() {
	db := database.SetUpConnection()
	r := repo.NewRepo(db)

	s := services.NewService(r)

	listen, err := net.Listen("tcp", ":5000")
	if err != nil {
		log.Fatal(err)
	}
	server := grpc.NewServer()

	rpc.SetUpServerControllers(server, s)

	err = server.Serve(listen)
	if err != nil {
		logrus.Fatal(err)
	}
}
