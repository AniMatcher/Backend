CREATE TABLE Chat (
    user1 uuid REFERENCES Auth(uuid),
    chatroom uuid PRIMARY KEY,
    content TEXT,
    created_at TIMESTAMP,
);