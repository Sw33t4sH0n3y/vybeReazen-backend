from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os
import psycopg2

import psycopg2.extras

from auth_middleware import token_required

from auth_blueprint import authentication_blueprint
from soundscapes_blueprint import soundscapes_blueprint
from sessions_blueprint import sessions_blueprint
from favorites_blueprint import favorites_blueprint
from frequencies_blueprint import frequencies_blueprint

from db_helpers import get_db_connection, validate_volume, get_safeguards

app = Flask(__name__)
CORS(app)
app.register_blueprint(authentication_blueprint)
app.register_blueprint(soundscapes_blueprint)
app.register_blueprint(sessions_blueprint)
app.register_blueprint(favorites_blueprint)
app.register_blueprint(frequencies_blueprint)

def get_db_connection():
    connection = psycopg2.connect(
        host='localhost',
        database=os.getenv('POSTGRES_DATABASE'),
        user=os.getenv('POSTGRES_USERNAME'),
        password=os.getenv('POSTGRES_PASSWORD')
    )
    return connection

#  USERS 

@app.route('/users')
@token_required
def users_index():
    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("SELECT id, username FROM users;")
    users = cursor.fetchall()
    connection.close()
    return jsonify(users), 200

@app.route('/users/<user_id>')
@token_required
def users_show(user_id):
    if int(user_id) != g.user["id"]:
        return jsonify({"err": "Unauthorized"}), 403
    connection = get_db_connection()
    connection = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("SELECT id, username FROM users WHERE id = %s;", (user_id,))
    users = cursor.fetchone()
    connection.close()
    if user is None:
        return jsonify({"err": "User not found"}), 404
    return jsonify(users), 200

# AUDIO FILES

@app.route('/audio/<filename>')
def serve_audio(filename):
    return send_from_directory('audio', filename)

#  SAFEGUARDS

@app.route('/safeguards')
def safeguards():
    return jsonify(get_safeguards()), 200

#  ROOT

@app.route('/')
def root():
    return jsonify ({"message": "Healing Frequencies API", "status": "running"}), 200


# Run our application, by default on port 5000
app.run()