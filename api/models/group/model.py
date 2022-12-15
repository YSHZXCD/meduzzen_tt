from bson import ObjectId

from api.extensions.custom_exception import ModelException
from api.extensions.default_model import DefaultModel
from api.extensions.mongo_init import mongo
from api.models.user.model import User


class Group(DefaultModel):
    table = mongo.db.group

    def __init__(self, _id, group_name, users):
        self._id = _id
        self.group_name = group_name
        self.users = users

    @classmethod
    def create_group(cls, params):
        ins = cls.from_dict(params)
        if cls.is_valid(ins):
            if cls.find_one({"group_name": ins.group_name}):
                raise ModelException("Group with this name is already exist")

            params["users"] = []
            return cls.create_record(params)

    @classmethod
    def add_user(cls, group_id, user_id):
        if group := cls.find_by_id(group_id):
            if ObjectId(user_id) in group.users:
                raise ModelException("This user is already in list")
            cls.table.update_one(
                {"_id": ObjectId(group_id)}, {"$push": {"users": ObjectId(user_id)}}
            )
            return cls.find_by_id(group_id)
        raise ModelException("Group with this id doesnt exist")

    @classmethod
    def remove_user(cls, group_id, user_id):
        if group := cls.find_by_id(group_id):
            if ObjectId(user_id) not in group.users:
                raise ModelException("This user is not in group")
            cls.table.update_one(
                {"_id": ObjectId(group_id)}, {"$pull": {"users": ObjectId(user_id)}}
            )
            return cls.find_by_id(group_id)
        raise ModelException("Group with this id doesnt exist")

    @classmethod
    def check_user_in_group(cls, user_id, group_name):
        if User.find_by_id(user_id):
            if group := cls.find_one({"group_name": group_name}):
                if ObjectId(user_id) in group["users"]:
                    return True
                return False

    @classmethod
    def remove_group(cls, group_id):
        if cls.find_by_id(group_id):
            cls.table.delete_one({"_id": ObjectId(group_id)})
            return "Group has been deleted"

    @classmethod
    def from_dict(cls, _dict):
        return cls(
            _dict.get("_id") if _dict.get("_id") else None,
            _dict["group_name"],
            _dict.get("users") if _dict.get("users") else [],
        )

    @classmethod
    def from_json(cls, _json):
        return cls(
            _json.get("_id") if _json.get("_id") else None,
            _json["group_name"],
            _json.get("users") if _json.get("users") else [],
        )

    def to_json(self):
        return {"_id": self._id, "group_name": self.group_name, "users": self.users}

    def to_json_safe(self):
        return {
            "_id": str(self._id),
            "group_name": self.group_name,
            "users": [User.find_by_id(i).to_json_safe() for i in self.users],
        }

    def is_valid(self):
        if not (isinstance(self.group_name, str) and isinstance(self.users, list)):
            raise ModelException("Invalid parameters")
        return True
