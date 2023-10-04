-- Users table
create table
  Users (
    id bigint primary key generated always as identity,
    uuid uuid references auth (uuid),
    username text references auth (username),
    gender varchar(2) not null check (gender in ('M', 'F', 'NB')),
    sex_pref varchar(1) not null check (sex_pref in ('A', 'B', 'C', 'D', 'E', 'F', 'G')),
    genre text not null,
    bio text not null
  );

-- Auth table
create table
  auth (
    uuid uuid default gen_random_uuid () primary key,
    email text unique not null,
    username text unique
  );
