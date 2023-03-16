package controllers

import (
	"encoding/json"
	"github.com/anton-uvarenko/cinema/broker-service/internal/pkg"
	"github.com/sirupsen/logrus"
	"net/http"
	"net/rpc"
	"strings"
)

type PassRecoveryController struct {
	client *rpc.Client
}

func NewPassRecoveryController(client *rpc.Client) *PassRecoveryController {
	return &PassRecoveryController{
		client: client,
	}
}

type EmailPayload struct {
	Email string `json:"email"`
}

type CodePayload struct {
	Email string `json:"email"`
	Code  int    `json:"code"`
}

type PassRecoveryResponse struct {
	Jwt string `json:"jwt"`
}

type PasswordPayload struct {
	Id       int
	Password string `json:"password"`
}

func (c *PassRecoveryController) SendCode(w http.ResponseWriter, r *http.Request) {
	payload := EmailPayload{}
	err := json.NewDecoder(r.Body).Decode(&payload)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	var resp int
	err = c.client.Call("PassRecoveryController.SendRecoveryCode", payload.Email, &resp)
	if err != nil {
		fail := pkg.CustToPkgError(err.Error())
		http.Error(w, fail.Error(), fail.Code())
		return
	}
}

func (c *PassRecoveryController) VerifyCode(w http.ResponseWriter, r *http.Request) {
	payload := CodePayload{}
	err := json.NewDecoder(r.Body).Decode(&payload)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	resp := PassRecoveryResponse{}
	err = c.client.Call("PassRecoveryController.VerifyRecoveryCode", payload, &resp)
	if err != nil {
		logrus.Error(err)
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
	payload := PasswordPayload{}
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

	payload.Id = id

	var resp int
	err = c.client.Call("PassRecoveryController.UpdatePassword", payload, &resp)
	if err != nil {
		fail := pkg.CustToPkgError(err.Error())
		http.Error(w, fail.Error(), fail.Code())
		return
	}
}
