package rpc

import (
	"github.com/anton-uvarenko/cinema/authorization-service/internal/services"
	"github.com/anton-uvarenko/cinema/authorization-service/internal/transport/rpc/controllers"
	"net/rpc"
)

func SetUpServerControllers(services *services.Service) {
	_ = rpc.Register(controllers.NewAuthController(services.AuthService))
	_ = rpc.Register(controllers.NewVerificationController(services.VerificationService))
	_ = rpc.Register(controllers.NewPassRecoveryController(services.PasswordRecoveryService))
	//rpc.HandleHTTP()
}
