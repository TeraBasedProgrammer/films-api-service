package middleware

import (
	"github.com/anton-uvarenko/cinema/broker-service/internal/core"
	"github.com/anton-uvarenko/cinema/broker-service/internal/pkg"
	"net/http"
	"strings"
)

type AuthMiddleware struct {
	UserType []core.UserType
	Recovery bool
}

func (m AuthMiddleware) TokenVerify(next http.Handler) http.Handler {
	fn := func(w http.ResponseWriter, r *http.Request) {
		token := strings.Split(r.Header.Get("Authorization"), " ")[1]
		if len(token) == 0 {
			http.Error(w, "no jwt", http.StatusUnauthorized)
			return
		}

		err := pkg.Verify(token, m.UserType, m.Recovery)

		if err != nil {
			http.Error(w, err.Error(), http.StatusForbidden)
			return
		}

		next.ServeHTTP(w, r)
	}

	return http.HandlerFunc(fn)
}
