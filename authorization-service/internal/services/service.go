package services

import "github.com/anton-uvarenko/cinema/authorization-service/internal/core/repo"

type Service struct {
	SignInService *SignInService
	SignUpService *SignUpService
}

func NewService(repo *repo.Repo) *Service {
	return &Service{
		SignInService: NewSignInService(repo),
		SignUpService: NewSignUpService(repo),
	}
}
