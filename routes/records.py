from flask import Blueprint, request, jsonify, g
from database.db import get_db
from security.authorization import require_auth

records_bp = Blueprint("records", __name__)


# Create a record
@records_bp.route("/records", methods=["POST"])
@require_auth
def create_record():

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Invalid JSON body"}), 400

    if set(data.keys()) != {"title", "body"}:
        return jsonify({"error": "Title and body are required"}), 400

    title = data["title"]
    body = data["body"]

    if not isinstance(title, str) or not isinstance(body, str):
        return jsonify({"error": "Title and body must be strings"}), 400

    title = title.strip()

    if not title or not 1 <= len(title) <= 100:
        return jsonify({"error": "Invalid title length"}), 400

    if not 1 <= len(body) <= 5000:
        return jsonify({"error": "Invalid body length"}), 400

    conn = get_db()

    try:

        cursor = conn.execute(
            """
            INSERT INTO records (user_id, title, body)
            VALUES (?, ?, ?)
            """,
            (g.user_id, title, body)
        )

        conn.commit()

        return jsonify({
            "message": "Record created successfully",
            "record_id": cursor.lastrowid
        }), 201

    finally:
        conn.close()


# Read a record
@records_bp.route("/records/<int:record_id>", methods=["GET"])
@require_auth
def get_record(record_id):

    conn = get_db()

    try:

        record = conn.execute(
            """
            SELECT id, user_id, title, body, created_at
            FROM records
            WHERE id = ?
            """,
            (record_id,)
        ).fetchone()

        if not record:
            return jsonify({"error": "Record not found"}), 404

        # Admin can access any record
        if g.role != "admin" and record["user_id"] != g.user_id:
            return jsonify({"error": "Record not found"}), 404

        return jsonify({
            "id": record["id"],
            "title": record["title"],
            "body": record["body"],
            "created_at": record["created_at"]
        }), 200

    finally:
        conn.close()
@records_bp.route("/records", methods=["GET"])
@require_auth
def list_records():

    conn = get_db()

    try:

        if g.role == "admin":

            records = conn.execute(
                """
                SELECT id, title, body, created_at
                FROM records
                ORDER BY id DESC
                """
            ).fetchall()

        else:

            records = conn.execute(
                """
                SELECT id, title, body, created_at
                FROM records
                WHERE user_id = ?
                ORDER BY id DESC
                """,
                (g.user_id,)
            ).fetchall()

        return jsonify([
            {
                "id": record["id"],
                "title": record["title"],
                "body": record["body"],
                "created_at": record["created_at"]
            }
            for record in records
        ]), 200

    finally:
        conn.close()        
@records_bp.route("/me", methods=["GET"])
@require_auth
def current_user():

    return jsonify({
        "username": g.username,
        "role": g.role,
        "user_id": g.user_id
    }), 200        