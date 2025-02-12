from flask import Blueprint, jsonify, request
from models import db, Student
from utils import create_response

student_bp = Blueprint("students", __name__)

# 🔹 Insert (Create) a New Student
@student_bp.route("/students", methods=["POST"])
def create_student():
    data = request.json
    if not all(k in data for k in ("name", "age", "grade")):
        return jsonify(create_response(status="error", message="Missing fields")), 400
    
    new_student = Student(name=data["name"], age=data["age"], grade=data["grade"])
    db.session.add(new_student)
    db.session.commit()

    return jsonify(create_response(data=new_student.to_dict(), message="Student created successfully")), 201


# 🔹 Get All Students
@student_bp.route("/students", methods=["GET"])
def get_students():
    students = Student.query.all()
    return jsonify(create_response(data=[student.to_dict() for student in students]))


# 🔹 Get a Specific Student by ID
@student_bp.route("/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify(create_response(status="error", data=None, message="Student not found")), 404
    return jsonify(create_response(data=student.to_dict()))


# 🔹 Update a Student
@student_bp.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify(create_response(status="error", message="Student not found")), 404

    data = request.json
    student.name = data.get("name", student.name)
    student.age = data.get("age", student.age)
    student.grade = data.get("grade", student.grade)
    
    db.session.commit()
    return jsonify(create_response(data=student.to_dict(), message="Student updated successfully"))


# 🔹 Delete a Student
@student_bp.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify(create_response(status="error", message="Student not found")), 404

    db.session.delete(student)
    db.session.commit()
    return jsonify(create_response(data=None, message="Student deleted successfully"))

