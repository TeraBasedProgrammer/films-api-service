package main

import (
	"github.com/anton-uvarenko/cinema/authorization-service/internal/core/database"
	"github.com/anton-uvarenko/cinema/authorization-service/internal/core/repo"
	"github.com/anton-uvarenko/cinema/authorization-service/internal/services"
	"github.com/anton-uvarenko/cinema/authorization-service/internal/transport/http"
	"github.com/sirupsen/logrus"
	"log"
)

func main() {
	db := database.SetUpConnection()
	r := repo.NewRepo(db)

	s := services.NewService(r)
	c := http.NewControllers(s)
	router := http.NewRouter(c)

	handler := router.SetUpRouts()
	server := http.InitHttpServer(handler)

	logrus.Info("Running server on port 80")
	log.Fatal(server.ListenAndServe())
}
