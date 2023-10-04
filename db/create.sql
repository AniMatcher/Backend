-- Users table
CREATE TABLE Users (
    uuid uuid REFERENCES Auth(uuid),
    username TEXT Auth(username),
    gender VARCHAR(2) NOT NULL CHECK (gender IN ('M', 'F', 'NB')),
    sex_pref VARCHAR(1) NOT NULL CHECK (sex_pref in ('A', 'B', 'C', 'D', 'E', 'F', 'G')),
    genre TEXT NOT NULL,
    bio TEXT NOT NULL
);

-- Auth table
CREATE TABLE Auth (
    uuid uuid default gen_random_uuid() PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    username TEXT UNIQUE,
    password_hash TEXT NOT NULL
);
