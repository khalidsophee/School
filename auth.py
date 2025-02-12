import uuid
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
from flask_jwt_extended import create_access_token, create_refresh_token

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    if not all(k in data for k in ("username", "password")):
        return jsonify({"status": "error", "message": "Missing fields"}), 400

    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"status": "error", "message": "User already exists"}), 409

    # Hash password
    password_hash = generate_password_hash(data["password"])
    session_id = str(uuid.uuid4())  # Generate a unique session ID

    # Create new user
    new_user = User(username=data["username"], password_hash=password_hash, session_id=session_id)
    db.session.add(new_user)
    db.session.commit()

    # Generate JWT Tokens
    access_token = create_access_token(identity=data["username"])
    refresh_token = create_refresh_token(identity=data["username"])

    return jsonify({
        "status": "success",
        "message": "User registered successfully",
        "session_id": session_id,
        "access_token": access_token,
        "refresh_token": refresh_token
    }), 201
