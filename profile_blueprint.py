from flask import Blueprint, request, jsonify, g
from db_helpers import get_db_connection
from auth_middleware import token_required
from main import upload_image

profile_blueprint = Blueprint('profile', __name__)

# Get Profile
@profile_blueprint.route('/profile', methods=['GET'])
@token_required
def get_profile():
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute('SELECT id, username, email, image_url, created_at FROM users WHERE is =%s', (g.user['id'],))

    row = cursor.fetchone()
    columns = [desc[0] for desc in cursor.description]
    user = dict(zip(columns, row))

    cursor.close()
    connection.close()

    return jsonify(user), 200

    # Upload Profile Pic
@profile_blueprint.route('/profile/image', methods=['POST'])
@token_required
def upload_profile_image():
    try:
        image = request.files.get('image')

        if not image:
            return jsonify({'error': 'No image provided'}), 400

        # Upload to Cloudinary
        image_url = upload_image(image)

        # Update database
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute('UPDATE users SET image_url = %s WHERE id = %s RETURNING id, username, email, image_url', (image_url, g.user['id']))

        row = cursor.fetchone()
        columns = [desc[0] for desc in cursor.description]
        user = dict(zip(columns, row))

        connection.commit()
        cursor.close()
        connection.close()

        return jsonify(user), 200

    except Exception as error:
        return jsonify({'error': str(error)}), 500

 # Delete profile picture
@profile_blueprint.route('/profile/image', methods=['DELETE'])
@token_required
def delete_profile_image():
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute('UPDATE users image_url = NULL WHERE id = %s', (g.user['id'],))

    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({'messge': 'Profile image removed'}), 200


