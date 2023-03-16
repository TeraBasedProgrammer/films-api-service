package pkg

import (
	"errors"
	"fmt"
	"github.com/anton-uvarenko/cinema/broker-service/internal/core"
	"github.com/golang-jwt/jwt"
	"github.com/sirupsen/logrus"
	"os"
	"strconv"
)

var ErrorInvalidToken = errors.New("invalid token")
var ErrorUserNotAllowed = errors.New("this user has not enough rights to access this endpoint")

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

func Verify(token string, userType []core.UserType, recovery bool) error {
	_, err := jwt.Parse(token, func(t *jwt.Token) (interface{}, error) {
		_, ok := t.Method.(*jwt.SigningMethodHMAC)
		if !ok {
			return nil, ErrorInvalidToken
		}

		claims, _ := t.Claims.(jwt.MapClaims)

		if claims["ps-recovery"] != recovery {
			return nil, ErrorInvalidToken
		}

		for _, v := range userType {
			if claims["userType"] == string(v) {
				return []byte(os.Getenv("SIGNATURE")), nil
			}
		}

		return nil, ErrorUserNotAllowed

	})

	return err
}
