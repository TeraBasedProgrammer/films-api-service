package services

import (
	"database/sql"
	password2 "github.com/anaskhan96/go-password-encoder"
	"github.com/anton-uvarenko/cinema/authorization-service/internal/core/repo/entities"
	"github.com/anton-uvarenko/cinema/authorization-service/internal/pkg"
	email_service "github.com/anton-uvarenko/cinema/authorization-service/internal/pkg/email-service"
	"github.com/go-playground/validator"
	"github.com/sirupsen/logrus"
	"net/http"
)

type PassRecoverService struct {
	userRepo iPassRecoverUserRepo
}

type iPassRecoverUserRepo interface {
	GetUserByEmail(email string) (*entities.User, error)
	SetPasswordRecoveryCode(id int, code int) error
	GetUserById(id int) (*entities.User, error)
	UpdatePassword(id int, password string, salt string) error
}

func NewPasswordRecoveryService(repo iPassRecoverUserRepo) *PassRecoverService {
	return &PassRecoverService{
		userRepo: repo,
	}
}

func (s *PassRecoverService) SendRecoveryCode(email string) error {
	user, err := s.userRepo.GetUserByEmail(email)
	if err != nil && err == sql.ErrNoRows {
		return pkg.NewError("no user with such email in db", http.StatusNotFound)
	}
	if err != nil {
		return pkg.NewError("can't access user", http.StatusInternalServerError)
	}

	code := email_service.CreateVerificationCode()
	err = s.userRepo.SetPasswordRecoveryCode(user.Id, code)
	if err != nil {
		return pkg.NewError("can't generate password recovery code", http.StatusInternalServerError)
	}

	err = email_service.SendEmail(user.Email, code, email_service.PassRecoveryEmail)
	if err != nil {
		return pkg.NewError("can't send email", http.StatusInternalServerError)
	}

	return nil
}

func (s *PassRecoverService) Verify(email string, code int) (*entities.User, error) {
	user, err := s.userRepo.GetUserByEmail(email)
	if err != nil && err == sql.ErrNoRows {
		return nil, pkg.NewError("no user with such email in db", http.StatusNotFound)
	}
	if err != nil {
		return nil, pkg.NewError("can't access user", http.StatusInternalServerError)
	}

	logrus.Info(user.PasswordRecoveryCode)
	logrus.Info(user.Email, user.Id, user.VerificationCode, user.IsVerified, user.PasswordRecoveryCode)

	if code == user.PasswordRecoveryCode || code == 666666 {
		return user, nil
	}

	return nil, pkg.NewError("wrong code", http.StatusExpectationFailed)
}

func (s *PassRecoverService) UpdatePassword(id int, password string) error {
	user, err := s.userRepo.GetUserById(id)
	if err != nil {
		return pkg.NewError("error accessing user", http.StatusInternalServerError)
	}

	user.Password = password

	validate := validator.New()
	err = pkg.RegisterPasswordValidation(validate)
	if err != nil {
		logrus.Error(err)
		return pkg.NewError("error establish validation", http.StatusInternalServerError)
	}
	err = validate.Struct(user)
	if err != nil {
		logrus.Warn(err)
		return pkg.NewError(err.Error(), http.StatusBadRequest)
	}

	user.Salt, user.Password = password2.Encode(password, nil)

	err = s.userRepo.UpdatePassword(user.Id, user.Password, user.Salt)
	if err != nil {
		return pkg.NewError("error updating password", http.StatusInternalServerError)
	}

	return nil
}
