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
	app.Use(middleware.Logger)

	//auth
	app.Route("/auth", func(router chi.Router) {
		router.Post("/signin", r.controllers.SignInController.SignIn)
		router.Post("/signup", r.controllers.SignUpController.SignUp)
	})

	//verification
	app.Route("/verify", func(router chi.Router) {
		router.Get("/send", r.controllers.VerificationController.SendCode)
		router.Post("/check", r.controllers.VerificationController.VerifyCode)
	})

	app.Route("/recover", func(router chi.Router) {
		router.Post("/send", r.controllers.PasswordRecoveryController.SendRecoveryCode)
		router.Post("/check", r.controllers.PasswordRecoveryController.VerifyRecoveryCode)
		router.Post("/change", r.controllers.PasswordRecoveryController.UpdatePassword)
	})

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
