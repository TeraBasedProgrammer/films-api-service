package main

import (
	"github.com/anton-uvarenko/cinema/authorization-service/internal/core/database"
	"github.com/anton-uvarenko/cinema/authorization-service/internal/core/repo"
	"github.com/anton-uvarenko/cinema/authorization-service/internal/services"
	"github.com/anton-uvarenko/cinema/authorization-service/internal/transport/http"
	"log"
)

func main() {
	db := database.SetUpConnection()
	r := repo.NewRepo(db)

	s := services.NewService(r)
	router := http.NewRouter(s)

	handler := router.SetUpRouts()
	server := http.InitHttpServer(handler)
	log.Fatal(server.ListenAndServe())
}
