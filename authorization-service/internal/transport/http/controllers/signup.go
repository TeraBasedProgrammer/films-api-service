package controllers

import (
	"encoding/json"
	"github.com/anton-uvarenko/cinema/authorization-service/internal/core/repo/entities"
	"github.com/anton-uvarenko/cinema/authorization-service/internal/pkg"
	"github.com/go-playground/validator"
	"github.com/sirupsen/logrus"
	"net/http"
)

type SignUpController struct {
	userService iSignUpService
}

func NewSignUpController(service iSignUpService) *SignUpController {
	return &SignUpController{
		userService: service,
	}
}

type iSignUpService interface {
	SignUp(user *entities.User) (string, error)
}

func (c *SignUpController) SignUp(w http.ResponseWriter, r *http.Request) {
	user := &entities.User{}
	err := json.NewDecoder(r.Body).Decode(user)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	v := validator.New()
	err = pkg.RegisterPasswordValidation(v)
	if err != nil {
		logrus.Error(err.Error())
		http.Error(w, "registering validation error", http.StatusInternalServerError)
		return
	}
	err = v.Struct(user)
	if err != nil {
		logrus.Info(err.Error())
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	token, err := c.userService.SignUp(user)
	if err != nil {
		logrus.Error(err)

		fail := err.(pkg.Error)
		http.Error(w, fail.Error(), fail.Code())
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
