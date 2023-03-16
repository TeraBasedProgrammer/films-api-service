package controllers

import (
	"encoding/json"
	"github.com/anton-uvarenko/cinema/broker-service/internal/pkg"
	"github.com/sirupsen/logrus"
	"net/http"
	"net/rpc"
	"strings"
)

type VerificationController struct {
	client *rpc.Client
}

func NewVerificationController(client *rpc.Client) *VerificationController {
	return &VerificationController{
		client: client,
	}
}

type VerificationPayload struct {
	Id   int `json:"-"`
	Code int `json:"code"`
}

func (c *VerificationController) SendCode(w http.ResponseWriter, r *http.Request) {
	token := strings.Split(r.Header.Get("Authorization"), " ")[1]
	id, err := pkg.ParseWithId(token)
	if err != nil {
		http.Error(w, "error parsing jwt", http.StatusInternalServerError)
	}

	var resp int
	err = c.client.Call("VerificationController.SendCode", id, &resp)
	if err != nil {
		logrus.Error(err)
		fail := pkg.CustToPkgError(err.Error())
		http.Error(w, fail.Error(), fail.Code())
		return
	}
}

func (c *VerificationController) VerifyCode(w http.ResponseWriter, r *http.Request) {
	payload := VerificationPayload{}
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

	payload.Id = id

	var resp int
	err = c.client.Call("VerificationController.VerifyCode", payload, &resp)
	if err != nil {
		fail := pkg.CustToPkgError(err.Error())
		http.Error(w, fail.Error(), fail.Code())
		return
	}
}
