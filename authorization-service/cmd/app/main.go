package main

import (
	"github.com/anton-uvarenko/cinema/authorization-service/internal/core/database"
	"github.com/anton-uvarenko/cinema/authorization-service/internal/core/repo"
	"github.com/anton-uvarenko/cinema/authorization-service/internal/services"
	rpc2 "github.com/anton-uvarenko/cinema/authorization-service/internal/transport/rpc"
	"github.com/sirupsen/logrus"
	"log"
	"net"
	"net/rpc"
)

func main() {
	db := database.SetUpConnection()
	r := repo.NewRepo(db)

	s := services.NewService(r)

	rpc2.SetUpServerControllers(s)

	//logrus.Fatal(http.ListenAndServe(":5000", nil))
	listen, err := net.Listen("tcp", "0.0.0.0:5000")
	if err != nil {
		log.Fatal(err)
	}
	defer listen.Close()
	for {
		rpcConn, err := listen.Accept()
		if err != nil {
			logrus.Error(err)
			continue
		}
		go rpc.ServeConn(rpcConn)
	}
}
