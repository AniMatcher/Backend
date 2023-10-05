create table auth (
    uuid uuid default gen_random_uuid() primary key,
    username text unique,
    email text unique,
    password_hash text
)

create table
  users (
    uuid uuid primary key,
    username text unique,
    gender char(2) not null,
    sex_pref char(1) not null,
    genre text,
    bio text,
    foreign key (uuid) references auth (uuid),
    check (gender in ('M', 'F', 'NB')),
    check (sex_pref in ('A', 'B', 'C', 'D', 'E', 'F', 'G'))
  );

create table useranimes (
    uuid uuid primary key,
    aid integer unique,
    foreign key(uuid) references users(uuid),
    foreign key(aid) references animes(aid)
);
