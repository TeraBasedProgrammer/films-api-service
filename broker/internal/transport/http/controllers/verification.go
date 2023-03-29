package controllers

import (
	"encoding/json"
	"github.com/anton-uvarenko/cinema/broker-service/internal/pkg"
	"github.com/anton-uvarenko/cinema/broker-service/protobufs/auth"
	"github.com/sirupsen/logrus"
	"golang.org/x/net/context"
	"net/http"
	"strings"
	"time"
)

type VerificationController struct {
	client auth.VerificationClient
}

func NewVerificationController(client auth.VerificationClient) *VerificationController {
	return &VerificationController{
		client: client,
	}
}

func (c *VerificationController) SendCode(w http.ResponseWriter, r *http.Request) {
	token := strings.Split(r.Header.Get("Authorization"), " ")[1]
	logrus.Info(token)

	id, err := pkg.ParseWithId(token)
	if err != nil {
		http.Error(w, "error parsing jwt", http.StatusInternalServerError)
	}

	logrus.Info(id)

	payload := auth.IdPayload{
		Id: int32(id),
	}

	logrus.Info(payload)

	ctx, cancel := context.WithTimeout(context.Background(), time.Second*3)
	defer cancel()

	_, err = c.client.SendCode(ctx, &payload)
	if err != nil {
		fail := pkg.CustToPkgError(err.Error())
		http.Error(w, fail.Error(), fail.Code())
		return
	}
}

func (c *VerificationController) VerifyCode(w http.ResponseWriter, r *http.Request) {
	payload := auth.VerificationPayload{}
	err := json.NewDecoder(r.Body).Decode(&payload)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	token := strings.Split(r.Header.Get("Authorization"), " ")[1]
	id, err := pkg.ParseWithId(token)
	if err != nil {
		http.Error(w, "error parsing jwt", http.StatusInternalServerError)
	}

	payload.Id = int32(id)

	ctx, cancel := context.WithTimeout(context.Background(), time.Second*3)
	defer cancel()

	_, err = c.client.VerifyCode(ctx, &payload)
	if err != nil {
		fail := pkg.CustToPkgError(err.Error())
		http.Error(w, fail.Error(), fail.Code())
		return
	}
}
