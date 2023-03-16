package entities

import (
	"context"
	"github.com/jmoiron/sqlx"
	"github.com/sirupsen/logrus"
	"time"
)

const DefaultExecTimeout = 5 * time.Second

type UserType string

const (
	Basic   UserType = "basic"
	Admin   UserType = "admin"
	Premium UserType = "premium"
)

type User struct {
	Id                   int       `json:"id" db:"id"`
	Avatar               string    `json:"avatar" db:"avatar_name"`
	Username             string    `json:"username" db:"username" validate:"required,alphanum,lte=8,gte=2"`
	Email                string    `json:"email" db:"email" validate:"required,email"`
	Password             string    `json:"password" db:"password" validate:"required,gte=8,lte=40,password"`
	Salt                 string    `json:"salt" db:"salt"`
	UserType             UserType  `json:"-" db:"user_type"`
	IsVerified           bool      `json:"-" db:"is_verified"`
	VerificationCode     int       `json:"-" db:"verification_code"`
	PasswordRecoveryCode int       `json:"-" db:"password_recovery_code"`
	CreatedAt            time.Time `json:"-" db:"created_at"`
	UpdatedAt            time.Time `json:"-" db:"updated_at"`
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
	INSERT INTO users (
	                   avatar_name, 
	                   username, email, 
	                   password, 
	                   salt, 
	                   created_at, 
	                   updated_at, 
	                   user_type,
	                   is_verified,
	                   verification_code)
	VALUES (
	        :avatar_name, 
	        :username, 
	        :email, 
	        :password, 
	        :salt, 
	        :created_at, 
	        :updated_at, 
	        :user_type,
	        :is_verified,
	        :verification_code)
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
	    id,  
	    email,
	    username,
	    verification_code
	FROM users
	WHERE id = $1
`
	user := &User{}
	err := r.db.GetContext(ctx, user, query, id)
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
	    id, 
	    avatar_name, 
	    username, 
	    email, 
		password_recovery_code,
		password,
		salt
	FROM USERS
	WHERE email = $1
`

	user := &User{}
	err := r.db.GetContext(ctx, user, query, email)
	if err != nil {
		return nil, err
	}

	return user, nil
}

func (r *UserRepo) MarkAsVerified(id int) error {
	ctx, cancel := context.WithTimeout(context.Background(), DefaultExecTimeout)
	defer cancel()

	query := `
	UPDATE users
	SET is_verified = true
	WHERE id = $1
`
	_, err := r.db.ExecContext(ctx, query, id)
	if err != nil {
		logrus.Error(err)
		return err
	}

	return nil
}

func (r *UserRepo) SetPasswordRecoveryCode(id int, code int) error {
	ctx, cancel := context.WithTimeout(context.Background(), DefaultExecTimeout)
	defer cancel()

	query := `
	UPDATE users
	SET password_recovery_code = $1
	WHERE id = $2
`
	_, err := r.db.ExecContext(ctx, query, code, id)
	if err != nil {
		logrus.Error(err)
		return err
	}

	return nil
}

func (r *UserRepo) UpdatePassword(id int, password string, salt string) error {
	ctx, cancel := context.WithTimeout(context.Background(), DefaultExecTimeout)
	defer cancel()

	query := `
	UPDATE users
	SET password = $1, salt = $2
	WHERE id = $3
`

	_, err := r.db.ExecContext(ctx, query, password, salt, id)
	if err != nil {
		logrus.Error(err)
		return err
	}

	return nil
}
