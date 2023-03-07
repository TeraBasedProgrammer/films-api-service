package services

import "github.com/anton-uvarenko/cinema/authorization-service/internal/core/repo"

type SignUpService struct {
	userRepo iSUUserRepo
}

type iSUUserRepo interface {
}

func NewSignUpService(repo *repo.Repo) *SignUpService {
	return &SignUpService{
		userRepo: repo.UserRepo,
	}
}
