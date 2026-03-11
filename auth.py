from flask import Blueprint, request, jsonify
from models import db, User
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
import bcrypt

auth = Blueprint("auth", __name__)

@auth.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"error": "Username and password are required"}), 400

    existing_user = User.query.filter_by(username=data["username"]).first()
    if existing_user:
        return jsonify({"error": "Username already taken"}), 409

    hashed_pw = bcrypt.hashpw(data["password"].encode("utf-8"), bcrypt.gensalt())

    new_user = User(
        username=data["username"],
        password=hashed_pw.decode("utf-8"),
        role=data.get("role", "user")
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


@auth.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"error": "Username and password are required"}), 400

    user = User.query.filter_by(username=data["username"]).first()

    if not user or not bcrypt.checkpw(data["password"].encode("utf-8"), user.password.encode("utf-8")):
        return jsonify({"error": "Invalid username or password"}), 401

    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={"role": user.role}
    )
    refresh_token = create_refresh_token(identity=str(user.id))

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token
    }), 200

@auth.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    current_user_id = get_jwt_identity()
    new_token = create_access_token(identity=current_user_id)
    return jsonify({"access_token": new_token}), 200    