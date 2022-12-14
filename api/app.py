from bson import ObjectId
from flask import Flask, jsonify
import click

from api.config import FlaskConfig
from api.extensions.custom_exception import ModelException, ViewException
from api.extensions.mongo_init import mongo


def create_app():
    app = Flask(__name__)
    app.config.from_object(FlaskConfig)
    configure_mongo(app)
    configure_blueprints(app)
    configure_extensions(app)

    @app.cli.command("create-admin")
    @click.argument("name")
    @click.argument("password")
    @click.argument("phone_number")
    def create_superuser(name, password, phone_number):
        from api.models.user.model import User
        from api.models.group.model import Group

        try:
            created_superuser = User.register_user(
                {"name": name, "password": password, "phone_number": phone_number}
            )
            created_group = Group.create_group({"group_name": "admin"})
            Group.create_group({"group_name": "employees"})
            Group.add_user(created_group._id, ObjectId(created_superuser._id))
            print(
                f"Superuser credentials: \nName: {name} \nPassword: {password} \nPhone number: {phone_number}"
            )
        except ModelException:
            print("Superuser with this credentials already exist")
            return

    @app.cli.command("create-manager")
    @click.argument("name")
    @click.argument("password")
    @click.argument("phone_number")
    def create_manager(name, password, phone_number):
        from api.models.user.model import User
        from api.models.group.model import Group

        try:
            created_manager = User.register_user(
                {"name": name, "password": password, "phone_number": phone_number}
            )
            created_group = Group.create_group({"group_name": "manager"})
            Group.add_user(created_group._id, ObjectId(created_manager._id))
            print(
                f"Manager credentials: \nName: {name} \nPassword: {password} \nPhone number: {phone_number}"
            )
        except ModelException:
            print("Manager with this credentials already exist")
            return

    return app


def configure_mongo(app):
    mongo.init_app(app)


def configure_extensions(app):
    @app.errorhandler(ModelException)
    @app.errorhandler(ViewException)
    def init_errors(error):
        return jsonify({"error_message": error.message, "code": error.code})


def configure_blueprints(app):
    from api.models.user.views import user
    from api.models.group.views import group
    from api.models.employee.views import employee
    from api.models.location.views import location

    app.register_blueprint(user)
    app.register_blueprint(group)
    app.register_blueprint(employee)
    app.register_blueprint(location)
