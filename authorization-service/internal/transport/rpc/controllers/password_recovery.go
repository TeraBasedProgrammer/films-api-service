package controllers

import (
	"github.com/anton-uvarenko/cinema/authorization-service/internal/core/repo/entities"
	"github.com/anton-uvarenko/cinema/authorization-service/internal/pkg"
	"github.com/sirupsen/logrus"
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

type codePayload struct {
	Code  int    `json:"code"`
	Email string `json:"email"`
}

type passwordPayload struct {
	Id       int
	Password string `json:"password"`
}

type PassRecoveryResponse struct {
	Jwt string
}

func (c *PassRecoveryController) SendRecoveryCode(email string) error {
	err := c.service.SendRecoveryCode(email)
	if err != nil {
		logrus.Error(err)
		return err
	}
	return nil
}

func (c *PassRecoveryController) VerifyRecoveryCode(code codePayload, resp *PassRecoveryResponse) error {
	user, err := c.service.Verify(code.Email, code.Code)
	if err != nil {
		logrus.Error(err)
		return err
	}

	token, err := pkg.NewJwt(user.Id, user.UserType, true)
	if err != nil {
		logrus.Error(err)
		return err
	}

	resp.Jwt = token
	return nil
}

func (c *PassRecoveryController) UpdatePassword(pass passwordPayload) error {
	err := c.service.UpdatePassword(pass.Id, pass.Password)
	if err != nil {
		logrus.Error(err)
		return err
	}

	return nil
}
