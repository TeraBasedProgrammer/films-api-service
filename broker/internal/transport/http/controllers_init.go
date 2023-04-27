package http

import (
	"github.com/anton-uvarenko/cinema/broker-service/internal/transport/grpc"
	"github.com/anton-uvarenko/cinema/broker-service/internal/transport/http/controllers"
)

type Controllers struct {
	AuthController         *controllers.AuthController
	VerificationController *controllers.VerificationController
	PassRecoveryController *controllers.PassRecoveryController
}

func NewControllers(clients grpc.AuthClients) *Controllers {
	return &Controllers{
		AuthController:         controllers.NewAuthController(clients.AuthClient),
		VerificationController: controllers.NewVerificationController(clients.VerificationClient),
		PassRecoveryController: controllers.NewPassRecoveryController(clients.PassRecoveryClient),
	}
}
