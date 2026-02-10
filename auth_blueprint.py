from flask import Blueprint, jsonify, request
from dotenv import load_dotenv
import os
import jwt
import bcrypt
import psycopg2, psycopg2.extras
from db_helpers import get_db_connection


authentication_blueprint = Blueprint('authentication_blueprint', __name__)

# Routes here:

@authentication_blueprint.route('/auth/sign-up', methods=['POST'])
def signup():
    try:
        new_user_data = request.get_json()
        print("Received data:", new_user_data)
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        cursor.execute("SELECT * FROM users WHERE username = %s;", (new_user_data["username"],))
        existing_user = cursor.fetchone()
        if existing_user:
            cursor.close()
            return jsonify({"err": "Username already taken"}), 400

        cursor.execute("SELECT * FROM users WHERE email = %s;", (new_user_data["email"],))
        existing_email = cursor.fetchone()
        if existing_email:
            cursor.close()
            return jsonify({"err": "Email already taken"}), 400

        hashed_password = bcrypt.hashpw(bytes(new_user_data["password"], 'utf-8'), bcrypt.gensalt())
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s) RETURNING id, username, email",
            (new_user_data["username"], new_user_data["email"], hashed_password.decode('utf-8'))
        )
        created_user = cursor.fetchone()
        connection.commit()
        connection.close()
        payload = {"username": created_user["username"], "id": created_user["id"]}
        token = jwt.encode({ "payload": payload }, os.getenv('JWT_SECRET'))
        return jsonify({"token": token}), 201
    except Exception as err:
        print("Error", err)
        return jsonify({"err": str(err)}), 401

@authentication_blueprint.route('/auth/sign-in', methods=["POST"])
def signin():
    try:
        sign_in_form_data = request.get_json()
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        cursor.execute("SELECT * FROM users WHERE username = %s;", (sign_in_form_data["username"],))
        existing_user = cursor.fetchone()

        if existing_user is None:
            return jsonify({"err": "Invalid credentials."}), 401
        password_is_valid = bcrypt.checkpw(bytes(sign_in_form_data["password"], 'utf-8'), bytes(existing_user["password"], 'utf-8'))
        if not password_is_valid:
            return jsonify({"err": "Invalid credentials."}), 401
        payload = {"username": existing_user["username"], "id": existing_user["id"]}
        token = jwt.encode({ "payload": payload }, os.getenv('JWT_SECRET'))
        return jsonify({"token": token}), 201
    except Exception as err:
        return jsonify({"err": str(err)}), 500
    finally:
        connection.close()