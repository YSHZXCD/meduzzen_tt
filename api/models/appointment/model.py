from bson import ObjectId

from api.extensions.custom_exception import ModelException
from api.extensions.default_model import DefaultModel
from api.extensions.mongo_init import mongo
from api.models.employee.model import Employee, Schedule


class Appointment(DefaultModel):
    table = mongo.db.appointments

    def __init__(self, _id, client_description, worker_id, date, start, end):
        self._id = _id
        self.client_description = client_description
        self.worker_id = worker_id
        self.date = date
        self.start = start
        self.end = end

    @classmethod
    def set_appointment(cls, emp_id, params):
        params["worker_id"] = ObjectId(emp_id)
        ins = cls.from_dict(params)
        if cls.is_valid(ins):
            if emp := Employee.find_by_id(emp_id):
                if emp.location:
                    if params["date"] in emp.schedule.keys():
                        inserted_id = cls.create_record(params)
                        Employee.table.update_one(
                            {"_id": ObjectId(emp_id)},
                            {"$push": {"appointment": ObjectId(inserted_id._id)}},
                        )
                        return Employee.find_by_id(emp_id)
                    raise ModelException("Invalid date")
                raise ModelException('Worker got not location')

    @classmethod
    def from_dict(cls, _dict):
        return cls(
            _dict.get("_id") if _dict.get("_id") else None,
            Description.set_description(_dict["client_description"]),
            _dict.get("worker_id") if _dict.get("worker_id") else None,
            _dict["date"],
            _dict["start"],
            _dict["end"],
        )

    @classmethod
    def from_json(cls, _json):
        return cls(
            _json.get("_id") if _json.get("_id") else None,
            Description.set_description(_json["client_description"]),
            _json.get("worker_id") if _json.get("worker_id") else None,
            _json["date"],
            _json["start"],
            _json["end"],
        )

    def to_json(self):
        return {
            "_id": self._id,
            "client_description": self.client_description,
            "worker_id": self.worker_id,
            "date": self.date,
            "start": self.start,
            "end": self.end,
        }

    def to_json_safe(self):
        return {
            "_id": str(self._id),
            "client_description": self.client_description,
            "worker_id": self.worker_id,
            "date": self.date,
            "start": self.start,
            "end": self.end,
        }

    def is_valid(self):
        if not (
            isinstance(self.client_description, Description)
            and isinstance(self.worker_id, ObjectId)
            and isinstance(self.date, str)
            and isinstance(self.start, str)
            and isinstance(self.end, str)
        ):
            raise ModelException("Invalid parameters")
        return True


class Description:
    def __init__(self, name, surname, phone_number):
        self.name = name
        self.surname = surname
        self.phone_number = phone_number

    @classmethod
    def set_description(cls, params):
        ins = cls.from_dict(params)
        if cls.is_valid(ins):
            return ins

    @classmethod
    def from_dict(cls, _dict):
        return cls(_dict["name"], _dict["surname"], _dict["phone_number"])

    def to_json(self):
        return {
            "name": self.name,
            "surname": self.surname,
            "phone_number": self.phone_number,
        }

    def is_valid(self):
        if not (
            isinstance(self.name, str)
            and isinstance(self.surname, str)
            and isinstance(self.phone_number, str)
        ):
            raise ModelException("Invalid parameters")
        return True
