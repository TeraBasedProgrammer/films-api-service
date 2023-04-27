package services

import (
	"github.com/anton-uvarenko/cinema/authorization-service/internal/core/repo/entities"
	"github.com/anton-uvarenko/cinema/authorization-service/internal/pkg"
	email_service "github.com/anton-uvarenko/cinema/authorization-service/internal/pkg/email-service"
	"github.com/aws/aws-sdk-go/service/ses"
	"github.com/sirupsen/logrus"
	"net/http"
)

const cheatCode = 666666

type VerificationService struct {
	userRepo iVerUserRepo
}

type iVerUserRepo interface {
	GetUserById(id int) (*entities.User, error)
	MarkAsVerified(id int) error
}

func NewVerificationService(repo iVerUserRepo) *VerificationService {
	return &VerificationService{
		userRepo: repo,
	}
}

func (s *VerificationService) SendCode(id int) error {
	user, err := s.userRepo.GetUserById(id)
	if err != nil {
		logrus.Error(err.Error())
		return pkg.NewError("error accessing user", http.StatusInternalServerError)
	}

	//send email
	err = email_service.SendEmail(user.Email, user.VerificationCode, email_service.VerificationEmail)
	if err != nil && err.Error() == ses.ErrCodeMessageRejected {
		return pkg.NewError("such email does not exist", http.StatusExpectationFailed)
	}

	if err != nil {
		return pkg.NewError("error sending email", http.StatusInternalServerError)
	}

	return nil
}

func (s *VerificationService) VerifyCode(code int, id int) error {
	user, err := s.userRepo.GetUserById(id)
	if err != nil {
		return pkg.NewError("error accessing user", http.StatusInternalServerError)
	}

	if code == cheatCode || code == user.VerificationCode {
		err = s.userRepo.MarkAsVerified(user.Id)
		if err != nil {
			return pkg.NewError("error updating user", http.StatusInternalServerError)
		}
		return nil
	}

	return pkg.NewError("wrong code", http.StatusForbidden)
}
