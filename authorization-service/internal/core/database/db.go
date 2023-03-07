package database

import (
	"github.com/jmoiron/sqlx"
	_ "github.com/lib/pq"
	"log"
	"os"
	"time"
)

const DefaultMaxOpenConns = 100
const DefaultConnLifeTime = 1 * time.Hour

func SetUpConnection() *sqlx.DB {
	connectStr := os.Getenv("SQL_CONTAINER_DSN")
	sqlDriver := os.Getenv("SQL_CONTAINER_DRIVER")
	db, err := sqlx.Open(sqlDriver, connectStr)

	if err != nil {
		panic(err)
	}

	db.SetMaxOpenConns(DefaultMaxOpenConns)
	db.SetConnMaxLifetime(DefaultConnLifeTime)

	log.Println("Successfully connected to db")
	return db
}
