package http

import (
	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
	"net/http"
	"time"
)

const DefaultWriteTimout = 60 * time.Second
const DefaultReadTimeout = 60 * time.Second
const DefaultStoreTimeout = 60 * time.Second

type Router struct {
	controllers *Controllers
}

func NewRouter(controllers *Controllers) *Router {
	return &Router{
		controllers: controllers,
	}
}

func (r *Router) SetUpRouts() http.Handler {
	app := chi.NewRouter()

	app.Use(middleware.Recoverer)

	app.Post("/auth/signin", r.controllers.SignInController.SignIn)
	app.Post("/auth/signup", r.controllers.SignUpController.SignUp)

	return app
}

func InitHttpServer(handler http.Handler) *http.Server {
	return &http.Server{
		Handler:           handler,
		Addr:              "0.0.0.0:80",
		WriteTimeout:      DefaultWriteTimout,
		ReadHeaderTimeout: DefaultReadTimeout,
	}
}
