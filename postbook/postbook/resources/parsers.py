import datetime

from flask_restful import reqparse


def get_user_credentials_parser():
    parser = reqparse.RequestParser()
    parser.add_argument("username", type=str, required=True, location="json")
    parser.add_argument("password", type=str, required=True, location="json")

    return parser


user_credentials_parser: reqparse.RequestParser = get_user_credentials_parser()


def get_post_parser():
    parser = reqparse.RequestParser()
    parser.add_argument("title", type=str, required=True, location="json")
    parser.add_argument("body", type=str, required=True, location="json")

    return parser


post_parser = get_post_parser()


def get_paginate_parser():
    parser = reqparse.RequestParser()
    parser.add_argument("start", type=int, default=0, location="args")
    parser.add_argument("limit", type=int, default=20, location="args")

    return parser


paginate_parser = get_paginate_parser()


def get_analytics_parser():
    parser = reqparse.RequestParser()
    parser.add_argument(
        "date_from", type=datetime.date.fromisoformat, required=True, location="args"
    )
    parser.add_argument(
        "date_to", type=datetime.date.fromisoformat, required=True, location="args"
    )

    return parser


analytics_parser = get_analytics_parser()
