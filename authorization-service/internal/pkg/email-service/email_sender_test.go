package email_service

import "testing"

func TestSendEmail(t *testing.T) {
	err := SendEmail("antontoxa90@gmail.com", 123123)
	if err != nil {
		t.Error(err)
	}
}
