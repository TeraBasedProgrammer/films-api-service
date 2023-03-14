package controllers

import (
	"encoding/json"
	"github.com/anton-uvarenko/cinema/broker-service/internal/pkg"
	"github.com/sirupsen/logrus"
	"net/http"
	"net/rpc"
)

type AuthController struct {
	client *rpc.Client
}

func NewAuthController(client *rpc.Client) *AuthController {
	return &AuthController{
		client: client,
	}
}

type SignInPayload struct {
	Email    string `json:"email"`
	Password string `json:"password"`
}

type SignUpPayload struct {
	Username string `json:"username"`
	Email    string `json:"email"`
	Password string `json:"password"`
}

type AuthResponse struct {
	Jwt string `json:"jwt"`
}

func (c *AuthController) SignIn(w http.ResponseWriter, r *http.Request) {
	payload := SignInPayload{}
	err := json.NewDecoder(r.Body).Decode(&payload)
	if err != nil {
		logrus.Info(err)
		http.Error(w, err.Error(), http.StatusBadGateway)
		return
	}

	logrus.Info(payload)

	resp := AuthResponse{}
	err = c.client.Call("AuthController.SignIn", payload, &resp)
	if err != nil {
		logrus.Error(err)
		//fail := err.(pkg.Error)
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	err = json.NewEncoder(w).Encode(&resp)
	if err != nil {
		http.Error(w, "error encoding response", http.StatusInternalServerError)
		return
	}
}

func (c *AuthController) SignUp(w http.ResponseWriter, r *http.Request) {
	payload := SignUpPayload{}
	err := json.NewDecoder(r.Body).Decode(&payload)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
	}

	resp := AuthResponse{}
	err = c.client.Call("AuthController.SignUp", payload, &resp)
	if err != nil {
		fail := err.(pkg.Error)
		http.Error(w, fail.Error(), fail.Code())
		return
	}

	err = json.NewEncoder(w).Encode(&resp)
	if err != nil {
		http.Error(w, "error encoding response", http.StatusInternalServerError)
		return
	}
}
