CREATE DATABASE healing_frequencies;
\connect healing_frequencies

DROP TABLE IF EXISTS sessions CASCADE;
DROP TABLE IF EXISTS soundscapes CASCADE;
DROP TABLE IF EXISTS users CASCADE;

CREATE TABLE users (
    id VARCHAR(36) PRIMARY KEY,
)