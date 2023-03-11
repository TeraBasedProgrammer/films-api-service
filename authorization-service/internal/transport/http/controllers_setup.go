package http

import (
	"github.com/anton-uvarenko/cinema/authorization-service/internal/services"
	"github.com/anton-uvarenko/cinema/authorization-service/internal/transport/http/controllers"
)

type Controllers struct {
	SignInController       *controllers.SignInController
	SignUpController       *controllers.SignUpController
	VerificationController *controllers.VerificationController
}

func NewControllers(service *services.Service) *Controllers {
	return &Controllers{
		SignInController:       controllers.NewSignInController(service.AuthService),
		SignUpController:       controllers.NewSignUpController(service.AuthService),
		VerificationController: controllers.NewVerificationController(service.VerificationService),
	}
}
