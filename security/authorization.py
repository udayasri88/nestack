from functools import wraps
from flask import request, jsonify, g
from database.db import get_db
from security.sessions import hash_session_token
from datetime import datetime, timezone


def require_auth(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):

        # Get session token from Authorization header
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Authentication required"}), 401

        token = auth_header.split(" ", 1)[1].strip()

        if not token:
            return jsonify({"error": "Invalid session token"}), 401

        # Hash the received token
        token_hash = hash_session_token(token)

        conn = get_db()

        try:

            # Find session in database
            session = conn.execute(
                """
                SELECT sessions.user_id, sessions.expires_at,
                       users.username, users.role
                FROM sessions
                JOIN users ON sessions.user_id = users.id
                WHERE sessions.token_hash = ?
                """,
                (token_hash,)
            ).fetchone()

            if not session:
                return jsonify({"error": "Invalid session"}), 401

            # Check session expiration
            expiry = datetime.fromisoformat(session["expires_at"])

            if expiry <= datetime.now(timezone.utc):
                conn.execute(
                    "DELETE FROM sessions WHERE token_hash = ?",
                    (token_hash,)
                )
                conn.commit()

                return jsonify({"error": "Session expired"}), 401

            # Store authenticated user information for this request
            g.user_id = session["user_id"]
            g.username = session["username"]
            g.role = session["role"]

        finally:
            conn.close()

        return f(*args, **kwargs)

    return decorated_function