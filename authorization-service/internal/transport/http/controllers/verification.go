package controllers

import (
	"encoding/json"
	"github.com/anton-uvarenko/cinema/authorization-service/internal/pkg"
	"net/http"
	"strings"
)

type verificationPayload struct {
	Code int `json:"code"`
}

type VerificationController struct {
	verificationService iVerificationService
}

type iVerificationService interface {
	SendCode(id int) error
	VerifyCode(code int, id int) error
}

func NewVerificationController(service iVerificationService) *VerificationController {
	return &VerificationController{
		verificationService: service,
	}
}

func (c *VerificationController) SendCode(w http.ResponseWriter, r *http.Request) {
	//get token
	bearer := r.Header.Get("Authorization")
	token := strings.Split(bearer, " ")[1]

	id, err := pkg.ParseWithId(token)
	if err != nil {
		http.Error(w, "error parsing jwt", http.StatusInternalServerError)
		return
	}

	err = c.verificationService.SendCode(id)
	if err != nil {
		fail := err.(pkg.Error)
		http.Error(w, fail.Error(), fail.Code())
		return
	}
}

func (c *VerificationController) VerifyCode(w http.ResponseWriter, r *http.Request) {
	code := &verificationPayload{}
	err := json.NewDecoder(r.Body).Decode(code)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	//get token
	bearer := r.Header.Get("Authorization")
	token := strings.Split(bearer, " ")[1]

	id, err := pkg.ParseWithId(token)
	if err != nil {
		http.Error(w, "error parsing jwt", http.StatusInternalServerError)
		return
	}

	err = c.verificationService.VerifyCode(code.Code, id)
	if err != nil {
		fail := err.(pkg.Error)
		http.Error(w, fail.Error(), fail.Code())
		return
	}
}
