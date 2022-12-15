from flask import Blueprint, jsonify, request

from api.extensions.check_token import access
from api.models.location.model import Location

location = Blueprint("location", __name__, url_prefix="/location")


@location.route("/add_location", methods=["POST"])
@access("manager")
def create_location():
    return jsonify(Location.create_location(request.json).to_json_safe())


@location.route(
    "/add_emp_to_location/<ObjectId:emp_id>/<ObjectId:location_id>", methods=["POST"]
)
@access("manager")
def add_emp_to_location(emp_id, location_id):
    return jsonify(Location.add_emp_on_location(emp_id, location_id).to_json_safe())


@location.route("/remove_emp_location/<ObjectId:emp_id>", methods=["DELETE"])
@access("manager")
def remove_location(emp_id):
    return jsonify({"status": Location.remove_emp_location(emp_id)})
