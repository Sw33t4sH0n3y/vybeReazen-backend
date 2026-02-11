from flask import Blueprint, request, jsonify, g
from db_helpers import get_db_connection
from auth_middleware import token_required
import uuid

favorites_blueprint = Blueprint('favorites', __name__)

# Get user's favorites
@favorites_blueprint.route('/favorites', methods=['GET'])
@token_required
def get_favorites():
    connection = get_db_connection()
    cursor = connection.cursor()

    query = (
        "SELECT s.*, f.created_at as favorited_at "
        "FROM favorites f "
        "JOIN soundscapes s ON f.soundscape_id = s.id "
        "WHERE f.user_id = %s "
        "ORDER BY f.created_at DESC"
    )
    cursor.execute(query, (g.user['id'],))

    columns = [desc[0] for desc in cursor.description]
    favorites = [dict(zip(columns, row)) for row in cursor.fetchall()]

    cursor.close()
    connection.close()

    return jsonify(favorites), 200

    # Add favorite
@favorites_blueprint.route('/favorites', methods=['POST'])
@token_required
def add_favorite():
    data = request.get_json()
    soundscape_id = data.get('soundscape_id')

    if not soundscape_id:
        return jsonify({'err': 'soundscape_id required'}), 400

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute('INSERT INTO favorites (user_id, soundscape_id) VALUES (%s, %s) RETURNING id', (g.user['id'], soundscape_id))

        favorite_id = cursor.fetchone()[0]
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({'id': favorite_id, 'message': 'Added to favorites'}), 201

    except Exception as e:
        connection.rollback()
        cursor.close()
        connection.close()
        return jsonify({'err': 'Already in favorites'}), 400

@favorites_blueprint.route('/favorites/<soundscape_id>', methods=['DELETE'])
@token_required
def remove_favorite(soundscape_id):
    connection = get_db_connection()
    cursor = connection.cursor()   

    cursor.execute('DELETE FROM favorites WHERE user_id = %s AND soundscape_id = %s', (g.user['id'], soundscape_id))

    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({'message': 'Removed from favorites'}),200         
