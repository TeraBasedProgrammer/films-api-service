package pkg

import (
	"fmt"
	"github.com/golang-jwt/jwt"
	"github.com/sirupsen/logrus"
	"strconv"
)

func ParseWithId(tokenString string) (int, error) {
	parser := jwt.Parser{}
	token, _, err := parser.ParseUnverified(tokenString, jwt.MapClaims{})
	if err != nil {
		logrus.Warning("error parsing jwt", err)
		return 0, err
	}

	claims := token.Claims.(jwt.MapClaims)
	userId, err := strconv.Atoi(fmt.Sprint(claims["id"]))
	if err != nil {
		logrus.Warning("error parsing jwt", err)
		return 0, err
	}

	return userId, nil
}
