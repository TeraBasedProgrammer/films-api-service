package rpc

import (
	"github.com/sirupsen/logrus"
	"net/rpc"
	"time"
)

const DefaultRetriesAmount = 5
const DefaultTryTimeout = 10 * time.Second

func ConnectServer(client chan<- *rpc.Client, dnsName, port string) {
	for i := 0; i < DefaultRetriesAmount; i++ {
		c, err := rpc.Dial("tcp", dnsName+":"+port)
		if err != nil {
			logrus.Error(err)
		}
		if c != nil {
			client <- c
			return
		}
		time.Sleep(DefaultTryTimeout)
	}

	//if can't establish connection stop the service
	logrus.Fatalf("Can't connect to %s on port %s", dnsName, port)
}
