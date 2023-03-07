package services

import "github.com/anton-uvarenko/cinema/authorization-service/internal/core/repo"

type SignInService struct {
	userRepo iSIUserRepo
}

type iSIUserRepo interface {
}

func NewSignInService(repo *repo.Repo) *SignInService {
	return &SignInService{
		userRepo: repo.UserRepo,
	}
}
