package controllers

import (
	"github.com/anton-uvarenko/cinema/authorization-service/internal/core/repo/entities"
	"github.com/anton-uvarenko/cinema/authorization-service/internal/pkg"
	"github.com/go-playground/validator"
	"github.com/sirupsen/logrus"
	"net/http"
)

type SignInPayload struct {
	Email    string `json:"email"`
	Password string `json:"password"`
}

type AuthController struct {
	service iAuthService
}

func NewAuthController(service iAuthService) *AuthController {
	return &AuthController{
		service: service,
	}
}

type iAuthService interface {
	SignIn(user *entities.User) (string, error)
	SignUp(user *entities.User) (string, error)
}

type AuthResponse struct {
	Jwt string
}

type SignUpPayload struct {
	Username string
	Email    string
	Password string
}

func (c *AuthController) SignIn(payload SignInPayload, resp *AuthResponse) error {
	user := &entities.User{
		Email:    payload.Email,
		Password: payload.Password,
	}

	token, err := c.service.SignIn(user)
	if err != nil {
		fail := err.(pkg.Error)
		return pkg.NewRpcError(fail.Error(), fail.Code())
	}

	resp.Jwt = token
	return nil
}

func (c *AuthController) SignUp(payload SignUpPayload, result *AuthResponse) error {
	user := &entities.User{
		Email:    payload.Email,
		Username: payload.Username,
		Password: payload.Password,
	}

	v := validator.New()
	err := pkg.RegisterPasswordValidation(v)
	if err != nil {
		logrus.Error(err.Error())

		return pkg.NewRpcError("validation registration error", http.StatusInternalServerError)
	}
	err = v.Struct(user)
	if err != nil {
		logrus.Info(err.Error())
		return pkg.NewRpcError(err.Error(), http.StatusBadRequest)
	}

	token, err := c.service.SignUp(user)
	if err != nil {
		logrus.Error(err)
		fail := err.(pkg.Error)
		return pkg.NewRpcError(fail.Error(), fail.Code())
	}

	result.Jwt = token
	return nil
}
