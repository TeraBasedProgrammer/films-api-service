CREATE TABLE users (
    id SERIAL PRIMARY KEY ,
    username VARCHAR(255),
    full_name VARCHAR(255),
    avatar_name VARCHAR(255),
    email VARCHAR(255),
    password TEXT,
    salt TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);