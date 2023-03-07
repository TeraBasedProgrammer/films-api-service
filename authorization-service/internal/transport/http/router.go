package http

import (
	"github.com/anton-uvarenko/cinema/authorization-service/internal/services"
	"github.com/go-chi/chi/v5"
	"net/http"
	"time"
)

const DefaultWriteTimout = 60 * time.Second
const DefaultReadTimeout = 60 * time.Second
const DefaultStoreTimeout = 60 * time.Second

type Router struct {
	service *services.Service
}

func NewRouter(service *services.Service) *Router {
	return &Router{
		service: service,
	}
}

func (r *Router) SetUpRouts() http.Handler {
	app := chi.NewRouter()

	return app
}

func InitHttpServer(handler http.Handler) *http.Server {
	return &http.Server{
		Handler:           handler,
		Addr:              "0.0.0.0:8080",
		WriteTimeout:      DefaultWriteTimout,
		ReadHeaderTimeout: DefaultReadTimeout,
	}
}
