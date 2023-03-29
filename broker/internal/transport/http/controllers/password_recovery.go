package controllers

import (
	"context"
	"encoding/json"
	"github.com/anton-uvarenko/cinema/broker-service/internal/pkg"
	"github.com/anton-uvarenko/cinema/broker-service/protobufs/auth"
	"net/http"
	"strings"
	"time"
)

type PassRecoveryController struct {
	client auth.PassVerifyClient
}

func NewPassRecoveryController(client auth.PassVerifyClient) *PassRecoveryController {
	return &PassRecoveryController{
		client: client,
	}
}

func (c *PassRecoveryController) SendCode(w http.ResponseWriter, r *http.Request) {
	payload := auth.EmailPayload{}
	err := json.NewDecoder(r.Body).Decode(&payload)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	ctx, cancel := context.WithTimeout(context.Background(), time.Second*3)
	defer cancel()

	_, err = c.client.SendRecoveryCode(ctx, &payload)
	if err != nil {
		fail := pkg.CustToPkgError(err.Error())
		http.Error(w, fail.Error(), fail.Code())
		return
	}
}

func (c *PassRecoveryController) VerifyCode(w http.ResponseWriter, r *http.Request) {
	payload := auth.CodePayload{}
	err := json.NewDecoder(r.Body).Decode(&payload)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	ctx, cancel := context.WithTimeout(context.Background(), time.Second*3)
	defer cancel()

	resp, err := c.client.VerifyRecoveryCode(ctx, &payload)
	if err != nil {
		fail := pkg.CustToPkgError(err.Error())
		http.Error(w, fail.Error(), fail.Code())
		return
	}

	w.Header().Add("Content-Type", "application/json")
	err = json.NewEncoder(w).Encode(resp)
	if err != nil {
		http.Error(w, "error encoding response", http.StatusInternalServerError)
		return
	}
}

func (c *PassRecoveryController) UpdatePassword(w http.ResponseWriter, r *http.Request) {
	payload := auth.PasswordPayload{}
	err := json.NewDecoder(r.Body).Decode(&payload)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	token := strings.Split(r.Header.Get("Authorization"), " ")[1]
	id, err := pkg.ParseWithId(token)
	if err != nil {
		http.Error(w, "error parsing jwt", http.StatusInternalServerError)
		return
	}

	payload.Id = int32(id)

	ctx, cancel := context.WithTimeout(context.Background(), time.Second*3)
	defer cancel()

	_, err = c.client.UpdatePassword(ctx, &payload)
	if err != nil {
		fail := pkg.CustToPkgError(err.Error())
		http.Error(w, fail.Error(), fail.Code())
		return
	}
}
