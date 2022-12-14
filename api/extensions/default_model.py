from bson import ObjectId

from api.extensions.custom_exception import ModelException


class DefaultModel:
    table = None

    def to_json(self):
        raise NotImplementedError

    def to_json_safe(self):
        raise NotImplementedError

    @classmethod
    def from_dict(cls, _dict):
        raise NotImplementedError

    @classmethod
    def from_json(cls, _json):
        raise NotImplementedError

    @classmethod
    def find_by_id(cls, _id):
        if res := cls.table.find_one({"_id": ObjectId(_id)}):
            return cls.from_dict(res)
        raise ModelException("Invalid id.")

    @classmethod
    def find_one(cls, params):
        if not params:
            params = {}

        data = cls.table.find_one(params)
        if data:
            return data

    @classmethod
    def create_record(cls, _obj):
        data = cls.table.insert_one(_obj)
        return cls.find_by_id(data.inserted_id)

    @classmethod
    def find(cls, params):
        if not params:
            params = {}

        data = cls.table.find(params)
        result = []
        for i in data:
            result.append(cls.from_dict(i))

        return result

    def is_valid(self):
        raise NotImplementedError
