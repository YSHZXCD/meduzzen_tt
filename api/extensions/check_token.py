import os
from functools import wraps

import jwt
from flask import request, g

from api.extensions.custom_exception import ModelException
from api.extensions.mongo_init import mongo
from api.models.group.model import Group


def access(props):
    def check_access_token(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not request.headers.get("Authorization"):
                raise ModelException("Invalid or corrupted token.")

            try:
                full_token = request.headers["Authorization"].split(" ")[1]
                decoded_token = jwt.decode(
                    full_token,
                    os.getenv("JWT_SECRET_KEY"),
                    algorithms=os.getenv("JWT_ALGORITHM"),
                )

                user = mongo.db.user.find_one({"name": decoded_token["name"]})
                if props == "admin":
                    if not Group.check_user_in_group(user["_id"], "admin"):
                        raise ModelException(
                            "You cant do it, since you are not an admin"
                        )
                if props == "manager":
                    if not Group.check_user_in_group(user["_id"], "manager"):
                        raise ModelException(
                            "You cant do it, since you are not a manager"
                        )

                if user:
                    g.user_id = str(user["_id"])

            except jwt.exceptions.DecodeError:
                raise ModelException("Invalid access token.")
            return func(*args, **kwargs)

        return wrapper

    return check_access_token
