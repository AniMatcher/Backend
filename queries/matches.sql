-- User liked another user table, includes column matched if they match
CREATE TABLE Matches (
    uuid uuid REFERENCES Auth(uuid),
    liked_user uuid REFERENCES Auth(uuid),
    match bool,
    PRIMARY KEY(uuid, liked_user)
);
