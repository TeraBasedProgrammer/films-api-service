package controllers

import (
	"github.com/anton-uvarenko/cinema/authorization-service/internal/pkg"
	"github.com/sirupsen/logrus"
)

type VerificationPayload struct {
	Id   int
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

func (c *VerificationController) SendCode(id int, resp *int) error {
	err := c.verificationService.SendCode(id)
	if err != nil {
		logrus.Error(err)
		fail := err.(pkg.Error)
		return pkg.NewRpcError(fail.Error(), fail.Code())
	}

	return nil
}

func (c *VerificationController) VerifyCode(payload VerificationPayload, resp *int) error {
	err := c.verificationService.VerifyCode(payload.Code, payload.Id)
	if err != nil {
		logrus.Error(err)
		fail := err.(pkg.Error)
		return pkg.NewRpcError(fail.Error(), fail.Code())
	}

	return nil
}
