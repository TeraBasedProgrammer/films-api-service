package entities

import (
	"context"
	"github.com/jmoiron/sqlx"
	"time"
)

const DefaultExecTimeout = 5 * time.Second

type User struct {
	Id        int       `json:"id"`
	Avatar    string    `json:"avatar"`
	Username  string    `json:"username"`
	Email     string    `json:"email"`
	Password  string    `json:"password"`
	Salt      string    `json:"salt"`
	CreatedAt time.Time `json:"-"`
	UpdatedAt time.Time `json:"-"`
}

type UserRepo struct {
	db *sqlx.DB
}

func NewUserRepo(db *sqlx.DB) *UserRepo {
	return &UserRepo{db: db}
}

func (r *UserRepo) AddUser(user *User) error {
	ctx, cancel := context.WithTimeout(context.Background(), DefaultExecTimeout)
	defer cancel()

	query := `
	INSERT INTO users (avatar_name, username, email, password, salt, created_at, updated_at)
	VALUES (?, ?, ?, ?, ?, ?, ?)
`
	_, err := r.db.ExecContext(
		ctx,
		query,
		user.Email,
		user.Username,
		user.Email,
		user.Password,
		user.Salt,
		user.CreatedAt,
		user.UpdatedAt,
	)

	return err
}

func (r *UserRepo) GetUserById(id int) (*User, error) {
	ctx, cancel := context.WithTimeout(context.Background(), DefaultExecTimeout)
	defer cancel()

	query := `
	SELECT FROM users
	WHERE id = ?
`
	user := &User{}
	err := r.db.SelectContext(ctx, user, query, id)
	if err != nil {
		return nil, err
	}

	return user, nil
}
