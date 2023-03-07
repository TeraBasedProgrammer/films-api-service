#!/bin/bash
local="postgresql://postgres:123456@localhost:5432/cinema?sslmode=disable"
remote="postgresql://postgres:MPaMKl1JVssd5BQk1iFn@database-1.cdcjcrzx6s07.eu-central-1.rds.amazonaws.com:5432"

if [[ $1 == "local" ]]; then
  echo $local
  migrate -database $local -path ../migrations up
elif [[ $1 == "remote" ]]; then
  migrate -database $remote -path ../migrations up
fi