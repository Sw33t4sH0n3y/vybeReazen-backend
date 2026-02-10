from flask import Blueprint, jsonify, request, g
from datetime import datetime
import psycopg2
import psycopg2.extras
import os
import uuid
from auth_middleware import token_required
from db_helpers import get_db_connection, validate_volume, get_safeguards

sessions_blueprint = Blueprint('sessions', __name__)


@sessions_blueprint.route('/sessions', methods=['POST'])
@token_required
def create_session():
    data = request.get_json()
    session_id = str(uuid.uuid4())
    user_id = g.user["id"]
    soundscape_id = data.get("soundscape_id")
    volume_used = data.get("volume_used", 0.75)

    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("""
        INSERT INTO sessions(id, user_id, soundscape_id, volume_used)
        VALUES (%s, %s, %s, %s)
        RETURNING *
    """, (session_id, user_id, soundscape_id, volume_used))
    
    session = cursor.fetchone()
    connection.commit()
    connection.close()
    return jsonify(session), 201

@sessions_blueprint.route('/sessions/<session_id>', methods=['PATCH'])
@token_required
def update_session(session_id):
    data = request.get_json()
    user_id = g.user["id"]
    ended_at = data.get("ended_at",datetime.utcnow())
    duration_actual = data.get("duration_actual", 0)
    completed = data.get("completed", False)

    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("""
        UPDATE sessions
        SET ended_at = %s, duration_actual = %s, completed = %s
        WHERE id = %s AND user_id = %s 
        RETURNING *
    """, (ended_at, duration_actual, completed, session_id, user_id))

    session = cursor.fetchone()
    connection.commit()
    connection.close()

    if session is None:
        return jsonify({"err": "Session not found"}), 404
    return jsonify(session), 200

@sessions_blueprint.route('/sessions', methods=['GET'])
@token_required
def get_user_sessions():
    user_id = g.user["id"]
    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("""
        SELECT s.*,   sc.name AS soundscape_name, sc.category, sc.genre
        FROM sessions s
        JOIN soundscapes sc ON s.soundscape_id = sc.id
        WHERE s.user_id = %s
        ORDER BY s.started_at DESC
    """, (user_id,))
    sessions = cursor.fetchall()
    connection.close()
    return jsonify(sessions), 200              

@sessions_blueprint.route('/sessions/<session_id>', methods=['DELETE'])
@token_required
def delete_session(session_id):
    try:
        user_id = g.user["id"]
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)  

        cursor.execute(
            "DELETE FROM sessions WHERE id = %s AND user_id = %s RETURNING id",
            (session_id, user_id)
        )
        deleted = cursor.fetchone()
        connection.commit()
        connection.close()

        if deleted is None:
            return jsonify({"err": "Session not found"}), 404
        return jsonify({"message": "Session deleted"}), 200
    except Exception as err:
        return jsonify({"err": str(err)}), 500                                      