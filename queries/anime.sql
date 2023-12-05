create extension if not exists "uuid-ossp";
CREATE EXTENSION pg_trgm;

create table
  anime (
    aid serial primary key,
    anime_id integer unique not null,
    anime_name text not null,
    score float not null,
    genres text,
    type text,
    source text,
    rank float,
    synopsis text,
    aired text,
    rating text,
    popularity integer not null,
    scored_by float,
    members integer not null,
    favourites integer,
    image_url text
  );

ALTER TABLE anime ADD COLUMN ts_name tsvector
    GENERATED ALWAYS AS (to_tsvector('english', anime_name)) STORED;

--creates index to help with trigram search
create index if not exists ts_idx on anime using gin (ts_name) tablespace pg_default;
create index if not exists trigram_anime_search on anime using gin (anime_name gin_trgm_ops) tablespace pg_default;

--this method allows for autocomplete search based on anime_name first
create or replace function anime_autocomplete_search (query text) returns TABLE (anime_name text, aid integer, anime_id integer, image_url text) as $$
  SELECT anime_name,aid,anime_id,image_url FROM anime ORDER BY similarity(anime_name, query) DESC, anime_name LIMIT 5;
$$ language sql;

--This method allow the swipes page to send one api request only to get all potential matches
create or replace function get_potential_matches (user_id uuid, gdr varchar) returns TABLE (uuid uuid,username text, gender varchar, sex_pref varchar, genre text, bio text, image_profile text, image_urls text) 
as 
$$ 
  select u1.uuid, u1.username, gender, sex_pref, genre, bio, image_profile, array_agg(image_url) as image_urls from users u1, user_animes, anime
  where  
  u1.uuid = user_animes.uuid
  AND user_animes.aid = anime.aid
  AND u1.uuid <> user_id
  AND u1.gender = gdr
  AND u1.uuid not in (select liked_user from matches m2 where m2.uuid = user_id)
  group by u1.uuid, u1.username, gender, sex_pref, genre, bio, image_profile
$$ language sql;