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


create index if not exists ts_idx on anime using gin (ts_name) tablespace pg_default;
create index if not exists trigram_anime_search on anime using gin (anime_name gin_trgm_ops) tablespace pg_default;

create or replace function anime_autocomplete_search (query text) returns TABLE (anime_name text, aid integer, anime_id integer, image_url text) as $$
  SELECT anime_name,aid,anime_id,image_url FROM anime ORDER BY similarity(anime_name, query) DESC, anime_name LIMIT 5;
$$ language sql;

