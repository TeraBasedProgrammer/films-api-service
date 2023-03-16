package pkg

import (
	"fmt"
	"github.com/anton-uvarenko/cinema/authorization-service/internal/core/repo/entities"
	"github.com/golang-jwt/jwt"
	"github.com/sirupsen/logrus"
	"os"
	"strconv"
	"time"
)

func NewJwt(id int, userType entities.UserType, recovery bool) (string, error) {
	claims := jwt.MapClaims{
		"exp":         time.Now().Add(time.Hour * 24 * 7).Unix(),
		"id":          id,
		"userType":    userType,
		"ps-recovery": recovery,
	}
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	tokenString, err := token.SignedString([]byte(os.Getenv("SIGNATURE")))
	if err != nil {
		logrus.Info(err.Error())
		return "", err
	}

	return tokenString, nil
}

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
