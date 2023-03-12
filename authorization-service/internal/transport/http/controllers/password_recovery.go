package controllers

import (
	"encoding/json"
	"github.com/anton-uvarenko/cinema/authorization-service/internal/core/repo/entities"
	"github.com/anton-uvarenko/cinema/authorization-service/internal/pkg"
	"github.com/sirupsen/logrus"
	"net/http"
	"strings"
)

type PassRecoveryController struct {
	service iPassRecoveryService
}

type iPassRecoveryService interface {
	SendRecoveryCode(email string) error
	Verify(email string, code int) (*entities.User, error)
	UpdatePassword(id int, password string) error
}

func NewPassRecoveryController(service iPassRecoveryService) *PassRecoveryController {
	return &PassRecoveryController{
		service: service,
	}
}

type emailPayload struct {
	Email string `json:"email"`
}

type codePayload struct {
	Code  int    `json:"code"`
	Email string `json:"email"`
}

type passwordPayload struct {
	Password string `json:"password"`
}

func (c *PassRecoveryController) SendRecoveryCode(w http.ResponseWriter, r *http.Request) {
	email := &emailPayload{}
	err := json.NewDecoder(r.Body).Decode(email)
	if err != nil {
		logrus.Warn(err)
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	err = c.service.SendRecoveryCode(email.Email)
	if err != nil {
		fail := err.(pkg.Error)
		http.Error(w, fail.Error(), fail.Code())
		return
	}
}

func (c *PassRecoveryController) VerifyRecoveryCode(w http.ResponseWriter, r *http.Request) {
	code := &codePayload{}
	err := json.NewDecoder(r.Body).Decode(code)
	if err != nil {
		logrus.Warn(err)
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	user, err := c.service.Verify(code.Email, code.Code)
	if err != nil {
		fail := err.(pkg.Error)
		http.Error(w, fail.Error(), fail.Code())
		return
	}

	token, err := pkg.NewJwt(user.Id, user.Salt, user.UserType, true)
	if err != nil {
		logrus.Error(err)
		http.Error(w, "error creating jwt", http.StatusInternalServerError)
		return
	}

	err = json.NewEncoder(w).Encode(struct {
		Jwt string `json:"jwt"`
	}{
		Jwt: token,
	})
}

func (c *PassRecoveryController) UpdatePassword(w http.ResponseWriter, r *http.Request) {
	pass := &passwordPayload{}
	err := json.NewDecoder(r.Body).Decode(pass)
	if err != nil {
		logrus.Warn(err)
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	token := strings.Split(r.Header.Get("Authorization"), " ")[1]
	id, err := pkg.ParseWithId(token)
	if err != nil {
		logrus.Warn(err)
		http.Error(w, "error parsing jwt", http.StatusInternalServerError)
		return
	}

	err = c.service.UpdatePassword(id, pass.Password)
	if err != nil {
		fail := err.(pkg.Error)
		http.Error(w, fail.Error(), fail.Code())
		return
	}
}
