from bson import ObjectId

from api.extensions.custom_exception import ModelException
from api.extensions.default_model import DefaultModel
from api.extensions.mongo_init import mongo
from api.models.employee.model import Employee


class Location(DefaultModel):
    table = mongo.db.locations

    def __init__(self, _id, location_name, emp_on_location):
        self._id = _id
        self.location_name = location_name
        self.emp_on_location = emp_on_location

    @classmethod
    def create_location(cls, params):
        ins = cls.from_dict(params)
        if cls.find_one({"location_name": params["location_name"]}):
            raise ModelException("This location is already exists")

        if cls.is_valid(ins):
            return cls.create_record(params)

    @classmethod
    def remove_emp_location(cls, emp_id):
        if emp := Employee.find_by_id(emp_id):
            if emp.location:
                Employee.table.update_one(
                    {"_id": ObjectId(emp_id)}, {"$set": {"location": None}}
                )
                return "Location is clear"
            raise ModelException("This worker got no location")

    @classmethod
    def add_emp_on_location(cls, emp_id, location_id):
        if emp := Employee.find_by_id(emp_id):
            if loc := cls.find_by_id(location_id):
                if loc.emp_on_location:
                    raise ModelException("Location is not empty")
                cls.table.update_one(
                    {"_id": ObjectId(location_id)},
                    {"$set": {"emp_on_location": ObjectId(emp_id)}},
                )
                Employee.table.update_one(
                    {"_id": ObjectId(emp_id)},
                    {"$set": {"location": ObjectId(location_id)}},
                )
                return cls.find_by_id(location_id)

    @classmethod
    def from_dict(cls, _dict):
        return cls(
            _dict.get("_id") if _dict.get("_id") else None,
            _dict["location_name"],
            _dict.get("emp_on_location") if _dict.get("emp_on_location") else None,
        )

    @classmethod
    def from_json(cls, _json):
        return cls(
            _json.get("_id") if _json.get("_id") else None,
            _json["location_name"],
            _json.get("emp_on_location") if _json.get("emp_on_location") else None,
        )

    def to_json(self):
        return {
            "_id": self._id,
            "location_name": self.location_name,
            "emp_on_location": self.emp_on_location,
        }

    def to_json_safe(self):
        return {
            "_id": str(self._id),
            "location_name": self.location_name,
            "emp_on_location": str(self.emp_on_location),
        }

    def is_valid(self):
        if not (
            isinstance(self.location_name, str)
            and (
                isinstance(self.emp_on_location, ObjectId)
                or self.emp_on_location is None
            )
        ):
            raise ModelException("Invalid parameters")
        return True
