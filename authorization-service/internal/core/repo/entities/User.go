package entities

import (
	"context"
	"github.com/jmoiron/sqlx"
	"github.com/sirupsen/logrus"
	"time"
)

const DefaultExecTimeout = 5 * time.Second

type User struct {
	Id        int       `json:"id" db:"id"`
	Avatar    string    `json:"avatar" db:"avatar_name"`
	Username  string    `json:"username" db:"username"`
	Email     string    `json:"email" db:"email"`
	Password  string    `json:"password" db:"password"`
	Salt      string    `json:"salt" db:"salt"`
	CreatedAt time.Time `json:"-" db:"created_at"`
	UpdatedAt time.Time `json:"-" db:"updated_at"`
}

type UserRepo struct {
	db *sqlx.DB
}

func NewUserRepo(db *sqlx.DB) *UserRepo {
	return &UserRepo{db: db}
}

func (r *UserRepo) AddUser(user *User) (*User, error) {
	ctx, cancel := context.WithTimeout(context.Background(), DefaultExecTimeout)
	defer cancel()

	query := `
	INSERT INTO users (avatar_name, username, email, password, salt, created_at, updated_at)
	VALUES (:avatar_name, :username, :email, :password, :salt, :created_at, :updated_at)
`
	rows, err := r.db.NamedQueryContext(
		ctx,
		query,
		user,
	)

	if err != nil {
		logrus.Error(err.Error())
		return nil, err
	}

	rowUser := &User{}
	for rows.Next() {
		err = rows.StructScan(rowUser)
	}
	if err != nil {
		logrus.Error(err.Error())
		return nil, err
	}

	return rowUser, err
}

func (r *UserRepo) GetUserById(id int) (*User, error) {
	ctx, cancel := context.WithTimeout(context.Background(), DefaultExecTimeout)
	defer cancel()

	query := `
	SELECT
	    id, avatar_name, username, email, password, salt, created_at, updated_at
	FROM users
	WHERE id = ?
`
	user := &User{}
	err := r.db.SelectContext(ctx, user, query, id)
	if err != nil {
		return nil, err
	}

	return user, nil
}

func (r *UserRepo) GetUserByEmail(email string) (*User, error) {
	ctx, cancel := context.WithTimeout(context.Background(), DefaultExecTimeout)
	defer cancel()

	query := `
	SELECT
	    id, avatar_name, username, email, password, salt, created_at, updated_at
	FROM USERS
	WHERE email = ?
`

	user := &User{}
	err := r.db.SelectContext(ctx, query, email)
	if err != nil {
		return nil, err
	}

	return user, nil
}
