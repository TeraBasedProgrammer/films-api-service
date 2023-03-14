package main

import (
	"github.com/anton-uvarenko/cinema/authorization-service/internal/core/database"
	"github.com/anton-uvarenko/cinema/authorization-service/internal/core/repo"
	"github.com/anton-uvarenko/cinema/authorization-service/internal/services"
	rpc2 "github.com/anton-uvarenko/cinema/authorization-service/internal/transport/rpc"
	"github.com/sirupsen/logrus"
	"net/http"
)

func main() {
	db := database.SetUpConnection()
	r := repo.NewRepo(db)

	s := services.NewService(r)

	rpc2.SetUpServerControllers(s)

	logrus.Fatal(http.ListenAndServe(":5000", nil))
}
