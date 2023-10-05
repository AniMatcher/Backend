create table animes (
    aid SERIAL primary key,
    anime_id integer unique,
    anime_name text,
    popularity integer,
    image_url text,
    score float
);