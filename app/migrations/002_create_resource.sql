CREATE TABLE IF NOT EXISTS resource (
    id SERIAL PRIMARY KEY,
    type_id INTEGER REFERENCES resource_type(id),
    name VARCHAR(255) NOT NULL,
    current_speed FLOAT NOT NULL
);