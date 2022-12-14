from flask import Blueprint, request, jsonify

from api.extensions.check_token import access
from api.models.employee.model import Employee, Schedule

employee = Blueprint("employee", __name__, url_prefix="/emp")


@employee.route("/create_employee", methods=["POST"])
@access("manager")
def register_employee():
    return jsonify(Employee.create_employee(request.json).to_json_safe())


@employee.route("/remove_employee/<ObjectId:emp_id>", methods=["DELETE"])
@access("manager")
def remove_employee(emp_id):
    return jsonify({'status': Employee.delete_employee(emp_id)})


@employee.route("/set_schedule/<ObjectId:emp_id>", methods=["POST"])
@access("manager")
def set_emp_schedule(emp_id):
    return jsonify(Schedule.set_schedule(emp_id, request.json).to_json_safe())


@employee.route("/get_emp_schedule/<ObjectId:emp_id>", methods=["GET"])
@access("manager")
def get_schedule(emp_id):
    return jsonify({"schedule": Employee.find_by_id(emp_id).schedule})
