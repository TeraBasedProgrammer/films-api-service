package controllers

import (
	"github.com/sirupsen/logrus"
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

func (c *VerificationController) SendCode(id int, resp *int) error {
	err := c.verificationService.SendCode(id)
	if err != nil {
		logrus.Error(err)
		return err
	}

	return nil
}

func (c *VerificationController) VerifyCode(payload verificationPayload, id int, resp *int) error {
	err := c.verificationService.VerifyCode(payload.Code, id)
	if err != nil {
		logrus.Error(err)
		return err
	}

	return nil
}
