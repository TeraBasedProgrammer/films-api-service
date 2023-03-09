package pkg

import (
	"github.com/go-playground/validator"
	"strings"
	"unicode"
)

const specialCharacters = " !\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"

func RegisterPasswordValidation(v *validator.Validate) error {
	err := v.RegisterValidation("password", validatePassword, false)
	return err
}

// password should contain at least 1 Uppercase letter,
// 1 lowercase letter, 1 digit and 1 special character
func validatePassword(fl validator.FieldLevel) bool {
	hasUpper := false
	hasLower := false
	hasDigit := false
	hasSpecial := false

	for _, v := range fl.Field().String() {
		if unicode.IsDigit(v) {
			hasDigit = true
			continue
		}
		if unicode.IsUpper(v) {
			hasUpper = true
			continue
		}
		if unicode.IsLower(v) {
			hasLower = true
			continue
		}
		if strings.Contains(specialCharacters, string(v)) {
			hasSpecial = true
			continue
		}
	}

	if hasUpper && hasLower && hasDigit && hasSpecial {
		return true
	}

	return false
}
