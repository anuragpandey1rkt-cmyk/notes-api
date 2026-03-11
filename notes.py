from flask import Blueprint, request, jsonify
from models import db, Note
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

notes = Blueprint("notes", __name__)

def get_current_user():
    user_id = int(get_jwt_identity())
    claims = get_jwt()
    return {"id": user_id, "role": claims.get("role")}

@notes.route("/notes", methods=["POST"])
@jwt_required()
def create_note():
    current_user = get_current_user()
    data = request.get_json()

    if not data or not data.get("title"):
        return jsonify({"error": "Title is required"}), 400

    new_note = Note(
        title=data["title"],
        content=data.get("content", ""),
        user_id=current_user["id"]
    )

    db.session.add(new_note)
    db.session.commit()

    return jsonify({"message": "Note created", "id": new_note.id}), 201


@notes.route("/notes", methods=["GET"])
@jwt_required()
def get_notes():
    current_user = get_current_user()

    if current_user["role"] == "admin":
        all_notes = Note.query.all()
    else:
        all_notes = Note.query.filter_by(user_id=current_user["id"]).all()

    result = []
    for note in all_notes:
        result.append({
            "id": note.id,
            "title": note.title,
            "content": note.content,
            "created_at": note.created_at.isoformat(),
            "updated_at": note.updated_at.isoformat(),
            "user_id": note.user_id
        })

    return jsonify(result), 200


@notes.route("/notes/<int:note_id>", methods=["PUT"])
@jwt_required()
def update_note(note_id):
    current_user = get_current_user()
    note = Note.query.get(note_id)

    if not note:
        return jsonify({"error": "Note not found"}), 404

    if note.user_id != current_user["id"]:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    if data.get("title"):
        note.title = data["title"]
    if data.get("content"):
        note.content = data["content"]

    db.session.commit()

    return jsonify({"message": "Note updated"}), 200


@notes.route("/notes/<int:note_id>", methods=["DELETE"])
@jwt_required()
def delete_note(note_id):
    current_user = get_current_user()
    note = Note.query.get(note_id)

    if not note:
        return jsonify({"error": "Note not found"}), 404

    if current_user["role"] != "admin" and note.user_id != current_user["id"]:
        return jsonify({"error": "Unauthorized"}), 403

    db.session.delete(note)
    db.session.commit()

    return jsonify({"message": "Note deleted"}), 200