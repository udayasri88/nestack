from flask import Blueprint, request, jsonify
from database.db import get_db
from security.password import hash_password
from security.password import verify_password
from security.sessions import (
    generate_session_token,
    hash_session_token,
    get_session_expiry
)

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json(silent=True)

    # Check whether valid JSON was provided
    if not isinstance(data, dict):
        return jsonify({"error": "Invalid JSON body"}), 400

    # Do not allow users to submit their own role
    if "role" in data:
        return jsonify({"error": "Role cannot be assigned during registration"}), 403

    # Validate required fields
    if set(data.keys()) != {"username", "password"}:
        return jsonify({"error": "Username and password are required"}), 400

    username = data["username"]
    password = data["password"]

    # Validate username
    if not isinstance(username, str):
        return jsonify({"error": "Username must be a string"}), 400

    username = username.strip()

    if not 3 <= len(username) <= 30:
        return jsonify({"error": "Username must contain 3-30 characters"}), 400

    # Validate password
    if not isinstance(password, str):
        return jsonify({"error": "Password must be a string"}), 400

    if not 12 <= len(password) <= 128:
        return jsonify({"error": "Password must contain 12-128 characters"}), 400

    # Connect to database
    conn = get_db()

    try:

        # Check whether username already exists
        existing_user = conn.execute(
            "SELECT id FROM users WHERE username = ?",
            (username,)
        ).fetchone()

        if existing_user:
            return jsonify({"error": "Username already exists"}), 409

        # Hash the password
        password_hash = hash_password(password)

        # Insert user into database
        conn.execute(
            """
            INSERT INTO users (username, password_hash)
            VALUES (?, ?)
            """,
            (username, password_hash)
        )

        conn.commit()

        return jsonify({
            "message": "User registered successfully"
        }), 201

    finally:
        conn.close()

@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Invalid JSON body"}), 400

    if set(data.keys()) != {"username", "password"}:
        return jsonify({"error": "Username and password are required"}), 400

    username = data["username"]
    password = data["password"]

    if not isinstance(username, str) or not isinstance(password, str):
        return jsonify({"error": "Invalid input types"}), 400

    if not username.strip() or not password:
        return jsonify({"error": "Username and password are required"}), 400

    conn = get_db()

    try:

        # Find the user
        user = conn.execute(
            "SELECT * FROM users WHERE username = ?",
            (username.strip(),)
        ).fetchone()

        # Check whether user exists
        if not user:
            return jsonify({"error": "Invalid credentials"}), 401

        # Verify password
        if not verify_password(user["password_hash"], password):

            return jsonify({"error": "Invalid credentials"}), 401

        # Generate session token
        token = generate_session_token()

        # Hash the token before storing it
        token_hash = hash_session_token(token)

        # Generate expiration time
        expires_at = get_session_expiry()

        # Store session in database
        conn.execute(
            """
            INSERT INTO sessions (user_id, token_hash, expires_at)
            VALUES (?, ?, ?)
            """,
            (user["id"], token_hash, expires_at)
        )

        conn.commit()

        return jsonify({
            "message": "Login successful",
            "session_token": token,
            "expires_at": expires_at
        }), 200

    finally:
        conn.close()        