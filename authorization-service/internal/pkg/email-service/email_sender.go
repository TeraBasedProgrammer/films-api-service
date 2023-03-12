package email_service

import (
	"bytes"
	"errors"
	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/credentials"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/ses"
	"github.com/sirupsen/logrus"
	"os"
	"text/template"
)

const (
	Sender  = "antontoxa90@gmail.com"
	Subject = "email verification"
	Charset = "UTF-8"
)

type EmailType string

const (
	VerificationEmail EmailType = "verification"
	PassRecoveryEmail EmailType = "recovery"
)

func setUpMailBody(code int, emailType EmailType) (string, error) {
	buffer := bytes.NewBuffer([]byte{})

	templateToParse := ""

	switch emailType {
	case VerificationEmail:
		templateToParse = "verification_email.gohtml"
		break
	case PassRecoveryEmail:
		templateToParse = "password_recovery_email.gohtml"
		break
	default:
		return "", errors.New("no such template")
	}

	//parse template
	data, err := template.ParseFiles("./templates/" + templateToParse)
	if err != nil {
		logrus.Error("parse error", err.Error())
		return "", err
	}
	err = data.Execute(buffer, code)
	if err != nil {
		logrus.Error("execute err", err.Error())
		return "", err
	}

	return buffer.String(), nil
}

func SendEmail(recipient string, code int, emailType EmailType) error {
	body, err := setUpMailBody(code, emailType)
	if err != nil {
		logrus.Error("error parsing template", err)
		return err
	}

	sess, err := session.NewSession(&aws.Config{
		CredentialsChainVerboseErrors: aws.Bool(true),
		Region:                        aws.String("eu-central-1"),
		Credentials: credentials.NewStaticCredentials(
			os.Getenv("AWS_ACCESS_KEY_ID"),
			os.Getenv("AWS_SECRET_ACCESS_KEY"),
			"",
		),
	})
	if err != nil {
		logrus.Error(err)
		return err
	}

	svs := ses.New(sess)

	input := &ses.SendEmailInput{
		Destination: &ses.Destination{
			ToAddresses: []*string{
				aws.String(recipient),
			},
		},
		Message: &ses.Message{
			Body: &ses.Body{
				Html: &ses.Content{
					Charset: aws.String(Charset),
					Data:    aws.String(body),
				},
				Text: &ses.Content{
					Charset: aws.String(Charset),
					Data:    aws.String("chudishe"),
				},
			},
			Subject: &ses.Content{
				Charset: aws.String(Charset),
				Data:    aws.String(Subject),
			},
		},
		Source: aws.String(Sender),
	}

	result, err := svs.SendEmail(input)
	if err != nil {
		logrus.Error(err)
		return err
	}

	logrus.Info(result)

	return nil
}
