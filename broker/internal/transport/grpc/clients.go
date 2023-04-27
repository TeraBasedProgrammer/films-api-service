package grpc

import (
	"github.com/anton-uvarenko/cinema/broker-service/protobufs/auth"
	"github.com/sirupsen/logrus"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
	"os"
	"time"
)

const DefaultRetriesAmount = 5
const DefaultTryTimeout = 10 * time.Second

type AuthClients struct {
	AuthClient         auth.AuthClient
	VerificationClient auth.VerificationClient
	PassRecoveryClient auth.PassVerifyClient
}

func ConnectAuthServer() AuthClients {
	conn, err := grpc.Dial(
		os.Getenv("DNS_AUTH")+":5000",
		grpc.WithTransportCredentials(insecure.NewCredentials()),
		grpc.WithBlock(),
	)
	if err != nil {
		logrus.Error(err)
		panic(err)
	}

	logrus.Info(conn.GetState())

	logrus.Info("connected to auth")

	clients := AuthClients{
		AuthClient:         auth.NewAuthClient(conn),
		VerificationClient: auth.NewVerificationClient(conn),
		PassRecoveryClient: auth.NewPassVerifyClient(conn),
	}

	return clients
}
