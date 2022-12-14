import hashlib
import os

import jwt

from api.extensions.custom_exception import ModelException
from api.extensions.default_model import DefaultModel
from api.extensions.mongo_init import mongo


class User(DefaultModel):
    table = mongo.db.user

    def __init__(self, _id, name, password, phone_number):
        self._id = _id
        self.name = name
        self.password = password
        self.phone_number = phone_number

    @classmethod
    def register_user(cls, params):
        ins = cls.from_dict(params)
        if cls.is_valid(ins):
            if cls.table.find_one(
                {"$or": [{"name": ins.name}, {"phone_number": ins.phone_number}]}
            ):
                raise ModelException("User with this credentials already exist")
            params["password"] = hashlib.sha256(params["password"].encode()).hexdigest()
            return cls.create_record(params)

    @classmethod
    def login_user(cls, params):
        if user := cls.find_one({"name": params["name"]}):
            hash_password = hashlib.sha256(params["password"].encode()).hexdigest()
            if hash_password == user["password"]:
                access_token = jwt.encode(
                    {"name": user["name"], "password": user["password"]},
                    str(os.getenv("JWT_SECRET_KEY")),
                    algorithm=str(os.getenv("JWT_ALGORITHM")),
                )
                return access_token
            raise ModelException("Invalid password", 404)
        raise ModelException("User not found", 404)

    @classmethod
    def from_dict(cls, _dict):
        return cls(
            _dict.get("_id") if _dict.get("_id") else None,
            _dict["name"],
            _dict["password"],
            _dict["phone_number"],
        )

    @classmethod
    def from_json(cls, _json):
        return cls(
            _json["_id"] if _json.get("_id") else None,
            _json["name"],
            _json["password"],
            _json["phone_number"],
        )

    def to_json(self):
        return {"_id": self._id, "name": self.name, "phone_number": self.phone_number}

    def to_json_safe(self):
        return {
            "_id": str(self._id),
            "name": self.name,
            "phone_number": self.phone_number,
        }

    def is_valid(self):
        if not (
            isinstance(self.name, str)
            and isinstance(self.password, str)
            and isinstance(self.phone_number, str)
        ):
            raise ModelException("Invalid parameters")
        return True
