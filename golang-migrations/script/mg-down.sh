#!/bin/bash

local="postgresql://postgres:123456@localhost:5432/cinema?sslmode=disable"
remote="postgresql://postgres:MPaMKl1JVssd5BQk1iFn@database-1.cdcjcrzx6s07.eu-central-1.rds.amazonaws.com:5432"

if [[ $1 == "local" ]]; then
  migrate -database $local -path ../migrations down
elif [[ $1 == "remote" ]]; then
  migrate -database $remote -path ../migrations down
fi