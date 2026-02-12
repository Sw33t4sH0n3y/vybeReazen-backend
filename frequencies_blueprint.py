from flask import Blueprint, jsonify
from db_helpers import get_db_connection
frequencies_blueprint = Blueprint('frequencies',__name__)

# Get All frequencies
@frequencies_blueprint.route('/frequencies', methods=['GET'])
def get_frequencies(): 
    connection =get_db_connection()
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM frequencies ORDER BY hz')

    columns = [desc[0] for desc in cursor.description]
    frequencies = [dict(zip(columns, row)) for row in cursor.fetchall()]

    cursor.close()
    connection.close()

    return jsonify(frequencies), 200
@frequencies_blueprint.route('/frequencies/<int:hz>', methods=['GET'])
def get_frequency(hz):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT *  FROM frequencies WHERE hz = %s', (hz,))

    row = cursor.fetchone()
    if not row:
        cursor.close()
        connection.close()
        return jsonify({'error': 'frequency not found'}), 404

    columns = [desc[0] for desc in cursor.description]
    frequency = dict(zip(columns, row))

    cursor.close()
    connection.close()    

    return jsonify(frequency), 200    

