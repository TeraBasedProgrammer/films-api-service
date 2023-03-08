package controllers

import (
	"encoding/json"
	"github.com/anton-uvarenko/cinema/authorization-service/internal/core/repo/entities"
	"github.com/anton-uvarenko/cinema/authorization-service/internal/pkg"
	"github.com/sirupsen/logrus"
	"net/http"
)

type SignInPayload struct {
	Email    string `json:"email"`
	Password string `json:"password"`
}

type SignInController struct {
	service iSignInService
}

func NewSignInController(service iSignInService) *SignInController {
	return &SignInController{
		service: service,
	}
}

type iSignInService interface {
	SignIn(user *entities.User) (string, error)
}

func (c *SignInController) SignIn(w http.ResponseWriter, r *http.Request) {
	payload := &SignInPayload{}
	err := json.NewDecoder(r.Body).Decode(payload)
	if err != nil {
		logrus.Error(err.Error())
		http.Error(w, "wrong input", http.StatusBadRequest)
		return
	}

	user := &entities.User{
		Email:    payload.Email,
		Password: payload.Password,
	}

	token, err := c.service.SignIn(user)
	if err != nil {
		logrus.Error(err.Error())
		http.Error(w, err.(pkg.Error).Error(), err.(pkg.Error).Code())
		return
	}

	err = json.NewEncoder(w).Encode(struct {
		Jwt string `json:"jwt"`
	}{
		Jwt: token,
	})

	if err != nil {
		logrus.Error(err.Error())
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
}
