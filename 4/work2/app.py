from pathlib import Path
from sqlite3 import Connection, OperationalError, connect
from typing import Tuple

from flask import Flask, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash

DB_PATH = Path(__file__).with_name("users.db")

app = Flask(__name__)


def init_db(db_path: Path = DB_PATH) -> None:
    try:
        with connect(db_path) as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL
                )
                """
            )
    except OperationalError as exc:
        # Log initialization errors so they surface immediately during setup.
        app.logger.exception("Failed to initialize database: %s", exc)
        raise


def get_db_connection() -> Connection:
    connection = connect(DB_PATH)
    connection.row_factory = lambda cursor, row: {cursor.description[idx][0]: value for idx, value in enumerate(row)}
    return connection


@app.post("/register")
def register() -> Tuple[str, int]:
    payload = request.get_json(silent=True) or {}
    username = (payload.get("username") or "").strip()
    password = payload.get("password") or ""

    if not username or not password:
        return jsonify({"error": "username and password are required"}), 400

    password_hash = generate_password_hash(password)

    try:
        with get_db_connection() as connection:
            connection.execute(
                "INSERT INTO users(username, password_hash) VALUES (?, ?)",
                (username, password_hash),
            )
            connection.commit()
    except OperationalError:
        app.logger.exception("Database write failed")
        return jsonify({"error": "internal server error"}), 500
    except Exception as exc:  # sqlite3.IntegrityError for duplicates
        app.logger.warning("Register failed for %s: %s", username, exc)
        return jsonify({"error": "user already exists"}), 409

    return jsonify({"message": "registration successful"}), 201


@app.post("/login")
def login() -> Tuple[str, int]:
    payload = request.get_json(silent=True) or {}
    username = (payload.get("username") or "").strip()
    password = payload.get("password") or ""

    if not username or not password:
        return jsonify({"error": "username and password are required"}), 400

    with get_db_connection() as connection:
        cursor = connection.execute(
            "SELECT password_hash FROM users WHERE username = ?", (username,)
        )
        row = cursor.fetchone()

    if not row or not check_password_hash(row["password_hash"], password):
        return jsonify({"error": "invalid credentials"}), 401

    return jsonify({"message": "login successful"}), 200


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
