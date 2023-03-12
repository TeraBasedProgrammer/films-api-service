package services

import (
	"database/sql"
	"github.com/anaskhan96/go-password-encoder"
	"github.com/anton-uvarenko/cinema/authorization-service/internal/core/repo/entities"
	"github.com/anton-uvarenko/cinema/authorization-service/internal/pkg"
	email_service "github.com/anton-uvarenko/cinema/authorization-service/internal/pkg/email-service"
	"net/http"
	"time"
)

type AuthService struct {
	userRepo iUserRepo
}

type iUserRepo interface {
	GetUserByEmail(email string) (*entities.User, error)
	AddUser(user *entities.User) (*entities.User, error)
}

func NewAuthService(repo iUserRepo) *AuthService {
	return &AuthService{
		userRepo: repo,
	}
}

func (s *AuthService) SignIn(user *entities.User) (string, error) {
	//check if user exists
	dbUser, err := s.userRepo.GetUserByEmail(user.Email)
	if err == sql.ErrNoRows {
		return "", pkg.NewError("no user with such email", http.StatusNotFound)
	}
	if err != nil {
		return "", pkg.NewError(err.Error(), http.StatusInternalServerError)
	}

	//verify password
	isVerified := password.Verify(user.Password, dbUser.Salt, dbUser.Password, nil)
	if !isVerified {
		return "", pkg.NewError("wrong password", http.StatusForbidden)
	}

	//create token
	token, err := pkg.NewJwt(dbUser.Id, dbUser.Salt, dbUser.UserType, false)
	if err != nil {
		return "", pkg.NewError("error occurred while creating jwt token", http.StatusInternalServerError)
	}

	return token, nil
}

func (s *AuthService) SignUp(user *entities.User) (string, error) {
	user.CreatedAt = time.Now()
	user.UpdatedAt = time.Now()
	user.Salt, user.Password = password.Encode(user.Password, nil)
	user.UserType = entities.Basic
	user.IsVerified = false
	user.VerificationCode = email_service.CreateVerificationCode()

	dbUser, err := s.userRepo.AddUser(user)
	if err != nil {
		return "", pkg.NewError("error creating user", http.StatusInternalServerError)
	}

	token, err := pkg.NewJwt(dbUser.Id, dbUser.Salt, dbUser.UserType, false)
	if err != nil {
		return "", pkg.NewError("error creating jwt", http.StatusInternalServerError)
	}

	return token, nil
}
