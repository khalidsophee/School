from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Student, User
from utils import create_response

student_bp = Blueprint("students", __name__)

# Helper function to validate session ID
def validate_session(username, session_id):
    user = User.query.filter_by(username=username, session_id=session_id).first()
    return user is not None

# 🔹 Insert (Create) a New Student
@student_bp.route("/students", methods=["POST"])
@jwt_required()
def create_student():
    data = request.json
    username = get_jwt_identity()
    session_id = request.headers.get("Session-ID")

    # Validate session ID
    if not session_id or not validate_session(username, session_id):
        return jsonify(create_response(status="error", message="Invalid session ID")), 401

    if not all(k in data for k in ("name", "age", "grade")):
        return jsonify(create_response(status="error", message="Missing fields")), 400
    
    new_student = Student(name=data["name"], age=data["age"], grade=data["grade"])
    db.session.add(new_student)
    db.session.commit()

    return jsonify(create_response(data=new_student.to_dict(), message="Student created successfully")), 201


# 🔹 Get All Students (Requires Token & Session ID)
@student_bp.route("/students", methods=["GET"])
@jwt_required()
def get_students():
    username = get_jwt_identity()
    session_id = request.headers.get("Session-ID")

    if not session_id or not validate_session(username, session_id):
        return jsonify(create_response(status="error", message="Invalid session ID")), 401

    students = Student.query.all()
    return jsonify(create_response(data=[student.to_dict() for student in students]))


# 🔹 Get a Specific Student by ID (Requires Token & Session ID)
@student_bp.route("/students/<int:student_id>", methods=["GET"])
@jwt_required()
def get_student(student_id):
    username = get_jwt_identity()
    session_id = request.headers.get("Session-ID")

    if not session_id or not validate_session(username, session_id):
        return jsonify(create_response(status="error", message="Invalid session ID")), 401

    student = Student.query.get(student_id)
    if not student:
        return jsonify(create_response(status="error", message="Student not found")), 404

    return jsonify(create_response(data=student.to_dict()))


# 🔹 Update a Student (Requires Token & Session ID)
@student_bp.route("/students/<int:student_id>", methods=["PUT"])
@jwt_required()
def update_student(student_id):
    username = get_jwt_identity()
    session_id = request.headers.get("Session-ID")

    if not session_id or not validate_session(username, session_id):
        return jsonify(create_response(status="error", message="Invalid session ID")), 401

    student = Student.query.get(student_id)
    if not student:
        return jsonify(create_response(status="error", message="Student not found")), 404

    data = request.json
    student.name = data.get("name", student.name)
    student.age = data.get("age", student.age)
    student.grade = data.get("grade", student.grade)
    
    db.session.commit()
    return jsonify(create_response(data=student.to_dict(), message="Student updated successfully"))


# 🔹 Delete a Student (Requires Token & Session ID)
@student_bp.route("/students/<int:student_id>", methods=["DELETE"])
@jwt_required()
def delete_student(student_id):
    username = get_jwt_identity()
    session_id = request.headers.get("Session-ID")

    if not session_id or not validate_session(username, session_id):
        return jsonify(create_response(status="error", message="Invalid session ID")), 401

    student = Student.query.get(student_id)
    if not student:
        return jsonify(create_response(status="error", message="Student not found")), 404

    db.session.delete(student)
    db.session.commit()
    return jsonify(create_response(data=None, message="Student deleted successfully"))
