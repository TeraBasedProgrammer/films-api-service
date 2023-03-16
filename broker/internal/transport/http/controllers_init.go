package http

import (
	"github.com/anton-uvarenko/cinema/broker-service/internal/transport/http/controllers"
	"net/rpc"
)

type Controllers struct {
	AuthController         *controllers.AuthController
	VerificationController *controllers.VerificationController
	PassRecoveryController *controllers.PassRecoveryController
}

func NewControllers(client *rpc.Client) *Controllers {
	return &Controllers{
		AuthController:         controllers.NewAuthController(client),
		VerificationController: controllers.NewVerificationController(client),
		PassRecoveryController: controllers.NewPassRecoveryController(client),
	}
}
