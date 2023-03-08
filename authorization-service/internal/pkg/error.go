package pkg

type Error struct {
	text     string
	httpCode int
}

func (e Error) Error() string {
	return e.text
}

func (e Error) Code() int {
	return e.httpCode
}

func NewError(message string, code int) Error {
	return Error{
		text:     message,
		httpCode: code,
	}
}
