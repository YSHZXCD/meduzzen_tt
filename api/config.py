import os


class FlaskConfig:
    DEBUG = os.getenv("DEBUG")
    SECRET_KEY = os.getenv("SECRET_KEY")

    MONGO_URI = "mongodb://{}:{}@{}:{}/{}".format(
        os.getenv("MONGO_USERNAME"),
        os.getenv("MONGO_PASSWORD"),
        os.getenv("MONGO_HOST"),
        os.getenv("MONGO_PORT"),
        os.getenv("MONGO_DB_NAME"),
    )
