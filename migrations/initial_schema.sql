CREATE DATABASE healing_frequencies;
\connect healing_frequencies

DROP TABLE IF EXISTS sessions CASCADE;
DROP TABLE IF EXISTS soundscapes CASCADE;
DROP TABLE IF EXISTS users CASCADE;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(100),
    role VARCHAR(20) DEFAULT 'user' NOT NULL,
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    last_login TIMESTAMP
);

CREATE TABLE soundscapes (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    category VARCHAR(50) NOT NULL,
    genre VARCHAR(50) NOT NULL,
    duration_seconds INTEGER NOT NULL,
    frequency_hz INTEGER NOT NULL,
    frequency_name VARCHAR(100) NOT NULL,
    tempo_bpm INTEGER NOT NULL,
    file_name VARCHAR(255) NOT NULL

);

CREATE TABLE sessions (
    id VARCHAR(36) PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    soundscape_id VARCHAR(36) NOT NULL REFERENCES soundscapes(id) ON DELETE CASCADE,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    ended_at TIMESTAMP,
    duration_actual INTEGER DEFAULT 0,
    completed BOOLEAN DEFAULT FALSE,
    volume_used REAL CHECK (volume_used BETWEEN 0 AND 1)
);

CREATE INDEX idx_sessions_user_id ON sessions(user_id);
CREATE INDEX idx_sessions_soundscape_id ON sessions(soundscape_id);
CREATE INDEX idx_sessions_started_at ON sessions(started_at DESC);
CREATE INDEX idx_users_email ON users(email);

INSERT INTO soundscapes(id, name, description, category, genre, duration_seconds, frequency_hz, frequency_name, tempo_bpm, file_name) VALUES
('1', 'Uptown Riddim', 'Upbeat dance with reggae and the 528Hz lovefrequency', 'fluid movement', 'reggae', 600, 528, 'Love Frequency', 75, '528Hz_Uptown_Riddim.mp3'),
('2', 'Tropical', 'Breathe with 432Hz natural harmony', 'relaxation', 'afro world', 900, 432, 'Natural Tuning', 95, '432Hz_Tropical.mp3'),
('3', 'Bodywork', 'Gentle drum rhythms with 639 connection frequency', 'massage', 'dub', 1200, 639, 'Connection', 80, '639Hz_Massage.mp3'),
('4', 'Deep inner stillness', 'Flowing rhythm of breath and nature with spiritual growth 741Hz frequency', 'meditation', 'spatial', 600, 741, 'Mental clarity', 65, '741Hz_Native_Flute.mp3'),
('5', 'Emotional Detox', 'Release, Rejuvenate, Rejoice', 'Mental Clearing', 'Quechua chanting and Flute', 600, 147, 'Emotional Detox', 82, '174Hz_Quechua_Flute.mp3')
