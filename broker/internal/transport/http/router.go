package http

import (
	"github.com/anton-uvarenko/cinema/broker-service/internal/core"
	md "github.com/anton-uvarenko/cinema/broker-service/internal/pkg/middleware"
	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
	"net/http"
	"time"
)

type Router struct {
	controllers *Controllers
}

const port = "80"
const ReadTimeout = 15 * time.Second
const WriteTimeout = 15 * time.Second

func NewRouter(controllers *Controllers) *Router {
	return &Router{
		controllers: controllers,
	}
}

func (r *Router) InitRoutes() http.Handler {
	app := chi.NewRouter()
	app.Use(middleware.Recoverer)
	app.Use(middleware.Logger)
	app.Use(middleware.Heartbeat("/ping"))

	app.Route("/auth", func(router chi.Router) {
		router.Post("/signin", r.controllers.AuthController.SignIn)
		router.Post("/signup", r.controllers.AuthController.SignUp)
	})

	app.Route("/verify", func(router chi.Router) {
		router.Get("/send", r.controllers.VerificationController.SendCode)
		router.Post("/check", r.controllers.VerificationController.VerifyCode)
	})

	app.Route("/recover", func(router chi.Router) {
		router.Post("/send", r.controllers.PassRecoveryController.SendCode)
		router.Post("/check", r.controllers.PassRecoveryController.VerifyCode)

		router.Group(func(rout chi.Router) {
			mid := md.AuthMiddleware{
				Recovery: true,
				UserType: []core.UserType{
					core.Premium,
					core.Basic,
					core.Admin,
				},
			}
			rout.Use(mid.TokenVerify)
			rout.Post("/change", r.controllers.PassRecoveryController.UpdatePassword)
		})
	})

	return app
}

func InitHttpServer(handler http.Handler) *http.Server {
	return &http.Server{
		Addr:         "0.0.0.0:" + port,
		ReadTimeout:  ReadTimeout,
		WriteTimeout: WriteTimeout,
		Handler:      handler,
	}
}