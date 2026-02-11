import os
import psycopg2


def get_db_connection():
    if 'ON_HEROKU' in os.environ:
        connection = psycopg2.connect(
            os.getenv('DATABASE_URL'), 
            sslmode='require'
        )
    else:
        connection = psycopg2.connect(
            host='localhost',
            database=os.getenv('POSTGRES_DATABASE'),
            user=os.getenv('POSTGRES_USERNAME'),
            password=os.getenv('POSTGRES_PASSWORD')
        )
    return connection

SAFEGUARDS = {
    "frequency_min_hz": 20,
    "frequency_max_hz": 1000,
    "max_master_volume": 0.90,
    "max_session_minutes": 120
}

def get_safeguards():
    return SAFEGUARDS

def validate_volume(volume):
    if volume > SAFEGUARDS["max_master_volume"]:
        return False, f"Volume exceeds max of {SAFEGUARDS['max_master_volume']}"
    return True, "Valid"

def validate_frequency(hertz):
    if hertz < SAFEGUARDS["frequency_min_hz"]:
        return False, f"Frequency too low (infrasound)"
    if hertz > SAFEGUARDS["frequency_max_hz"]:
        return False, f"Frequency exceeds safe range"
    return True, "Valid"

def consolidate_sessions_with_soundscapes(sessions_with_soundscapes):
    consolidated_sessions = []
    for session in sessions_with_soundscapes:
        session_exists = False
        for consolidated_session in consolidated_sessions:
            if session["id"] == consolidated_session["id"]:
                session_exists = True
                break
        if not session_exists:
            consolidated_sessions.append(session)
    return consolidated_sessions                                 

    