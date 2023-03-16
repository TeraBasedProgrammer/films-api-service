package pkg

import (
	"strconv"
	"strings"
)

type Error struct {
	text string
	code int
}

func (e Error) Error() string {
	return e.text
}

func (e Error) Code() int {
	return e.code
}

func NewError(err string, code int) Error {
	return Error{
		text: err,
		code: code,
	}
}

func CustToPkgError(err string) Error {
	parts := strings.Split(err, "; ")
	code, _ := strconv.Atoi(parts[1])

	return Error{
		text: parts[0],
		code: code,
	}
}
