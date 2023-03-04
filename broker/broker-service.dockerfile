FROM golang:1.19

WORKDIR /app

RUN go install github.com/cosmtrek/air@latest && \
    export GOPATH=$HOME/xxxxx && \
    export PATH=$PATH:$GOROOT/bin:$GOPATH/bin && \
    export PATH=$PATH:$(go env GOPATH)/bin \
COPY go.mod go.sum ./
RUN go mod download
COPY . .
CMD ["air", "-c", "air.toml"]