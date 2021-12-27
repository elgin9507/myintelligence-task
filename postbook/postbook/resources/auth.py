import datetime

from flask import request, jsonify
from flask_restful import Resource, marshal_with, fields
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    current_user,
)
from werkzeug.security import generate_password_hash, check_password_hash

from ..models import User
from .parsers import user_credentials_parser

user_activity_fields = {
    "last_login_date": fields.DateTime(dt_format="iso8601"),
    "last_activity": fields.DateTime(dt_format="iso8601"),
}


def create_tokens(username):
    access_token = create_access_token(username)
    refresh_token = create_refresh_token(username)

    return {"access_token": access_token, "refresh_token": refresh_token}


def parse_user_creds():
    parser = user_credentials_parser
    data = parser.parse_args(strict=True)

    return data


class UserRegisterResource(Resource):
    def post(self):
        credentials = parse_user_creds()
        username = credentials["username"]
        password = credentials["password"]

        if User.select().where(User.username == username):
            return {
                "message": {"username": "User with this uername already exists"}
            }, 400

        hashed_passwd = generate_password_hash(password)
        user = User(username=username, password=hashed_passwd)
        user.save()
        tokens = create_tokens(user.username)

        return {"id": user.id, "username": user.username, **tokens}


class UserLoginResource(Resource):
    def post(self):
        credentials = parse_user_creds()
        username = credentials["username"]
        password = credentials["password"]

        try:
            user = User.get(User.username == username)
        except User.DoesNotExist:
            return self.wrong_creds_resp()
        else:
            if not check_password_hash(user.password, password):
                return self.wrong_creds_resp()

        tokens = create_tokens(user.username)
        user.last_login_date = datetime.datetime.utcnow()
        user.save()

        return {"id": user.id, "username": user.username, **tokens}

    def wrong_creds_resp(self):
        return {"message": "Wrong credentials"}, 400


class RefreshTokenResource(Resource):
    @jwt_required(refresh=True)
    def post(self):
        identity = get_jwt_identity()
        access_token = create_access_token(identity)

        return {"access_token": access_token}


class UserActivityResource(Resource):
    @jwt_required()
    @marshal_with(user_activity_fields)
    def get(self):
        return current_user
