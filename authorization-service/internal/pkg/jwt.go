package pkg

import (
	"github.com/golang-jwt/jwt"
	"github.com/sirupsen/logrus"
	"time"
)

func NewJwt(id int, salt string) (string, error) {
	claims := jwt.MapClaims{
		"exp": time.Now().Add(time.Hour * 24 * 7),
		"id":  id,
	}
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	tokenString, err := token.SignedString([]byte(salt))
	if err != nil {
		logrus.Info(err.Error())
		return "", err
	}

	return tokenString, nil
}
