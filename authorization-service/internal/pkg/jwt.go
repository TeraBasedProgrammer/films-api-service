package pkg

import (
	"github.com/anton-uvarenko/cinema/authorization-service/internal/core/repo/entities"
	"github.com/golang-jwt/jwt"
	"github.com/sirupsen/logrus"
	"time"
)

func NewJwt(id int, salt string, userType entities.UserType) (string, error) {
	claims := jwt.MapClaims{
		"exp":      time.Now().Add(time.Hour * 24 * 7),
		"id":       id,
		"userType": userType,
	}
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	tokenString, err := token.SignedString([]byte(salt))
	if err != nil {
		logrus.Info(err.Error())
		return "", err
	}

	return tokenString, nil
}
