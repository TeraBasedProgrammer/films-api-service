package rpc

import (
	"github.com/anton-uvarenko/cinema/authorization-service/internal/services"
	"github.com/anton-uvarenko/cinema/authorization-service/internal/transport/rpc/controllers"
	"github.com/anton-uvarenko/cinema/authorization-service/protobufs/auth"
	"google.golang.org/grpc"
)

func SetUpServerControllers(server *grpc.Server, services *services.Service) {
	//_ = grpc.Register(controllers.NewAuthController(services.AuthService))
	//_ = grpc.Register(controllers.NewVerificationController(services.VerificationService))
	//_ = grpc.Register(controllers.NewPassRecoveryController(services.PasswordRecoveryService))
	//grpc.HandleHTTP()

	auth.RegisterAuthServer(server, controllers.NewAuthController(services.AuthService))
	auth.RegisterVerificationServer(server, controllers.NewVerificationController(services.VerificationService))
	auth.RegisterPassVerifyServer(server, controllers.NewPassRecoveryController(services.PasswordRecoveryService))
}
