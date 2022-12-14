from datetime import datetime

from bson import ObjectId

from api.extensions.custom_exception import ModelException
from api.extensions.default_model import DefaultModel
from api.extensions.mongo_init import mongo
from api.models.group.model import Group


class Employee(DefaultModel):
    table = mongo.db.employee

    def __init__(
        self,
        _id,
        name,
        schedule,
        speciality,
        location,
        appointments,
        phone_number,
        email,
    ):
        self._id = _id
        self.name = name
        self.schedule = schedule
        self.speciality = speciality
        self.location = location
        self.appointments = appointments
        self.phone_number = phone_number
        self.email = email

    @classmethod
    def create_employee(cls, params):
        ins = cls.from_dict(params)
        if cls.find_one({"phone_number": params["phone_number"]}):
            raise ModelException("Worker with this credentials already exists")

        if cls.is_valid(ins):
            params["schedule"] = {}
            params["appointment"] = []
            created_employee = cls.create_record(params)
            emp_group = Group.find_one({"group_name": "employees"})
            Group.add_user(emp_group["_id"], created_employee._id)
            return created_employee

    @classmethod
    def delete_employee(cls, emp_id):
        if cls.find_by_id(emp_id):
            group = Group.find_one({"group_name": "employees"})
            Group.remove_user(group["_id"], emp_id)
            cls.table.delete_one({'_id': ObjectId(emp_id)})
            return 'Employee has been deleted'

    @classmethod
    def from_dict(cls, _dict):
        return cls(
            _dict.get("_id") if _dict.get("_id") else None,
            _dict["name"],
            _dict.get("schedule") if _dict.get("schedule") else {},
            _dict["speciality"],
            _dict.get("location") if _dict.get("location") else None,
            _dict.get("appointment") if _dict.get("appointment") else [],
            _dict["phone_number"],
            _dict["email"],
        )

    @classmethod
    def from_json(cls, _json):
        return cls(
            _json.get("_id") if _json.get("_id") else None,
            _json["name"],
            _json.get("schedule") if _json.get("schedule") else {},
            _json["speciality"],
            _json.get("location") if _json.get("location") else None,
            _json.get("appointment") if _json.get("appointment") else [],
            _json["phone_number"],
            _json["email"],
        )

    def to_json(self):
        return {
            "_id": self._id,
            "name": self.name,
            "schedule": self.schedule,
            "speciality": self.speciality,
            "location": self.location,
            "appointments": self.appointments,
            "phone_number": self.phone_number,
            "email": self.email,
        }

    def to_json_safe(self):
        return {
            "_id": str(self._id),
            "name": self.name,
            "schedule": self.schedule,
            "speciality": self.speciality,
            "location": str(self.location),
            "appointments": [str(i) for i in self.appointments],
            "phone_number": self.phone_number,
            "email": self.email,
        }

    def is_valid(self):
        if not (
            isinstance(self.name, str)
            and (isinstance(self.schedule, dict) or self.schedule is None)
            and isinstance(self.speciality, str)
            and (isinstance(self.location, ObjectId) or self.location is None)
            and (isinstance(self.appointments, list) or self.appointments is None)
            and isinstance(self.phone_number, str)
            and isinstance(self.email, str)
        ):
            raise ModelException("Invalid parameters")
        return True


class Schedule:
    def __init__(self, schedule):
        self.schedule = schedule

    @classmethod
    def set_schedule(cls, emp_id, params):
        if Employee.find_by_id(emp_id):
            if res_schedule := cls.is_valid(params):
                Employee.table.update_one(
                    {"_id": ObjectId(emp_id)}, {"$set": {"schedule": res_schedule}}
                )
                return Employee.find_by_id(emp_id)

    @staticmethod
    def is_valid(params):
        res_schedule = {}

        if not isinstance(params, dict):
            raise ModelException("Invalid parameters")

        for i in params:
            try:
                date = datetime.strptime(i, "%d.%m.%Y").date()
            except ValueError:
                raise ModelException("Invalid date")

            if date <= datetime.now().date():
                raise ModelException("Invalid date")

            res_schedule[i] = {}
            for v in range(len(params[i])):
                res_schedule[i].update({str(v): params[i][v]})

        return res_schedule
