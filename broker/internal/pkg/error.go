package pkg

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
