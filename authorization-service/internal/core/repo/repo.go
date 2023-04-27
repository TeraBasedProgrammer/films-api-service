package repo

import (
	"github.com/anton-uvarenko/cinema/authorization-service/internal/core/repo/entities"
	"github.com/jmoiron/sqlx"
)

type Repo struct {
	UserRepo *entities.UserRepo
}

func NewRepo(db *sqlx.DB) *Repo {
	return &Repo{
		UserRepo: entities.NewUserRepo(db),
	}
}
