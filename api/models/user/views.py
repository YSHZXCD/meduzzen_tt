from flask import Blueprint, jsonify, request, g

from api.extensions.check_token import access
from api.models.appointment.model import Appointment
from api.models.employee.model import Employee
from api.models.user.model import User

user = Blueprint("user", __name__, url_prefix="/")


@user.route("/", methods=["POST"])
@access("admin")
def create_user():
    return jsonify(User.register_user(request.json).to_json_safe())


@user.route("/login", methods=["GET"])
def login_user():
    return jsonify({"access_token": User.login_user(request.json)})


@user.route("/get_emp", methods=["GET"])
def get_emp():
    return jsonify({"employees": [i.to_json_safe() for i in Employee.find({})]})


@user.route("/create_appointment/<ObjectId:emp_id>", methods=["POST"])
@access("admin")
def create_appointment(emp_id):
    return jsonify(Appointment.set_appointment(emp_id, request.json).to_json_safe())
