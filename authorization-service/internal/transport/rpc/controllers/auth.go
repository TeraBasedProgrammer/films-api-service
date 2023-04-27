package controllers

import (
	"context"
	"github.com/anton-uvarenko/cinema/authorization-service/internal/core/repo/entities"
	"github.com/anton-uvarenko/cinema/authorization-service/internal/pkg"
	"github.com/anton-uvarenko/cinema/authorization-service/protobufs/auth"
	"github.com/go-playground/validator"
	"github.com/sirupsen/logrus"
	"net/http"
)

type AuthController struct {
	auth.UnimplementedAuthServer
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

func (c *AuthController) SignIn(ctx context.Context, payload *auth.SignInPayload) (*auth.JwtResponse, error) {
	user := &entities.User{
		Email:    payload.Email,
		Password: payload.Password,
	}

	token, err := c.service.SignIn(user)
	if err != nil {
		fail := err.(pkg.Error)
		return nil, pkg.NewRpcError(fail.Error(), fail.Code())
	}

	return &auth.JwtResponse{
		Jwt: token,
	}, nil
}

func (c *AuthController) SignUp(ctx context.Context, payload *auth.SignUpPayload) (*auth.JwtResponse, error) {
	user := &entities.User{
		Email:    payload.Email,
		Username: payload.Username,
		Password: payload.Password,
	}

	v := validator.New()
	err := pkg.RegisterPasswordValidation(v)
	if err != nil {
		logrus.Error(err.Error())
		return nil, pkg.NewRpcError("validation registration error", http.StatusInternalServerError)

	}
	err = v.Struct(user)
	if err != nil {
		logrus.Info(err.Error())
		return nil, pkg.NewRpcError(err.Error(), http.StatusBadRequest)
	}

	token, err := c.service.SignUp(user)
	if err != nil {
		logrus.Error(err)
		fail := err.(pkg.Error)
		return nil, pkg.NewRpcError(fail.Error(), fail.Code())
	}

	return &auth.JwtResponse{
		Jwt: token,
	}, nil
}
