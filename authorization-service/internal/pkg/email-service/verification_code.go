package email_service

import (
	"math/rand"
	"time"
)

func CreateVerificationCode() int {
	rand.Seed(time.Now().Unix())
	code := (rand.Int() + 100000) % 100000
	return code
}
