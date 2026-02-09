from flask import Blueprint, jsonify, request
import psycopg2
import psycopg2.extras
import os
from auth_middleware import token_required

soundscapes_blueprint = Blueprint('soundscapes', __name__)

def get_db_connection():
    connection = psycopg2.connect(
        host='localhost',
        database=os.getenv('POSTGRES_DATABASE'),
        user=os.getenv('POSTGRES_USERNAME'),
        password=os.getenv('POSTGRES_PASSWORD')
    )
    return connection


@soundscapes_blueprint.route('/soundscapes', methods=['GET'])
@token_required
def get_all_soundscapes():
    category = request.args.get('category')
    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    if category:
        cursor.execute("SELECT * FROM soundscapes WHERE category = %s ORDER BY name"; (category))
    else:
        cursor.execute("SELECT *FROM soundscapes ORDER BY name")

    soundscapes = cursor.fetchall()
    connection.close()
    return jsonify(soundscapes), 200    
        
@soundscapes_blueprint.route('/soundscapes/<soundscape_id>', methods=['GET'])
@token_required
def get_soundscape(soundscape_id):
    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("SELECT* FROM soundscapes WHERE id  = %s", (soundscape_id,))
    soundscape = cursor.fetchone()
    connection.close()

    if soundscape is None:
        return jsonify({"err": "Soundscape not found"}), 404
    return jsonify(soundscape), 200            