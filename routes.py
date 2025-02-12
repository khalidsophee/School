from flask import Blueprint, jsonify, request
from models import db, Student
from utils import create_response

student_bp = Blueprint("students", __name__)

# 🔹 Insert (Create) a New Student
@student_bp.route("/students", methods=["POST"])
def create_student():
    try:
        data = request.json
        if not all(k in data for k in ("name", "age", "grade")):
            return jsonify(create_response(status="error", message="Missing fields")), 400
        
        new_student = Student(name=data["name"], age=data["age"], grade=data["grade"])
        db.session.add(new_student)
        db.session.commit()

        return jsonify(create_response(data=new_student.to_dict(), message="Student created successfully")), 201
    except Exception as e:
        db.session.rollback()
        return jsonify(create_response(status="error", message=str(e))), 500


# 🔹 Get All Students
@student_bp.route("/students", methods=["GET"])
def get_students():
    try:
        students = Student.query.all()
        if not students:
            return jsonify(create_response(status="success", data=[], message="No students found")), 200
        
        return jsonify(create_response(data=[student.to_dict() for student in students]))
    except Exception as e:
        return jsonify(create_response(status="error", message=str(e))), 500


# 🔹 Get a Specific Student by ID
@student_bp.route("/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    try:
        student = Student.query.get(student_id)
        if not student:
            return jsonify(create_response(status="error", message="Student not found")), 404
        
        return jsonify(create_response(data=student.to_dict()))
    except Exception as e:
        return jsonify(create_response(status="error", message=str(e))), 500


# 🔹 Update a Student
@student_bp.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    try:
        student = Student.query.get(student_id)
        if not student:
            return jsonify(create_response(status="error", message="Student not found")), 404

        data = request.json
        student.name = data.get("name", student.name)
        student.age = data.get("age", student.age)
        student.grade = data.get("grade", student.grade)
        
        db.session.commit()
        return jsonify(create_response(data=student.to_dict(), message="Student updated successfully"))
    except Exception as e:
        db.session.rollback()
        return jsonify(create_response(status="error", message=str(e))), 500


# 🔹 Delete a Student
@student_bp.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    try:
        student = Student.query.get(student_id)
        if not student:
            return jsonify(create_response(status="error", message="Student not found")), 404

        db.session.delete(student)
        db.session.commit()
        return jsonify(create_response(data=None, message="Student deleted successfully"))
    except Exception as e:
        db.session.rollback()
        return jsonify(create_response(status="error", message=str(e))), 500
