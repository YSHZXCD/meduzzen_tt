from flask import Blueprint, request, jsonify

from api.extensions.check_token import access
from api.models.group.model import Group

group = Blueprint("group", __name__, url_prefix="/group")


@group.route("/create_group", methods=["POST"])
@access("admin")
def create_group():
    return jsonify(Group.create_group(request.json).to_json_safe())


@group.route(
    "/add_user_to_group/<ObjectId:group_id>/<ObjectId:user_id>", methods=["POST"]
)
@access("admin")
def add_user_to_group(group_id, user_id):
    return jsonify(Group.add_user(group_id, user_id).to_json_safe())


@group.route("/remove_group/<ObjectId:group_id>", methods=["DELETE"])
@access("admin")
def remove_group(group_id):
    return jsonify({"status": Group.remove_group(group_id)})


@group.route("/remove_user/<ObjectId:group_id>/<ObjectId:user_id>", methods=["DELETE"])
@access("manager")
def remove_user(group_id, user_id):
    return jsonify(Group.remove_user(group_id, user_id).to_json_safe())
