from flask import Flask, request_finished
from flask_jwt_extended import JWTManager
from flask_restful import Api


from .resources import add_resources
from .utils import update_user_activity


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=False)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=False)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    api = Api(app)
    add_resources(api)

    jwt = JWTManager(app)

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        from .models import User

        username = jwt_data["sub"]

        return User.filter(User.username == username).first()

    request_finished.connect(update_user_activity, app)

    return app
