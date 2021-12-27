import datetime

from flask_restful import fields, Resource, marshal_with
from flask_jwt_extended import jwt_required, current_user

from ..models import Post, PostLike
from .utils import paginate, get_or_404, paginated_response
from .parsers import post_parser, analytics_parser


class DateField(fields.Raw):
    DEFAULT_FORMAT = "%Y-%m-%d"

    def __init__(self, *args, **kwargs):
        self.date_fmt = kwargs.pop("date_fmt", self.DEFAULT_FORMAT)
        super().__init__(*args, **kwargs)

    def format(self, value):
        date_str = value.strftime(self.date_fmt)

        return date_str


user_fields = {
    "id": fields.Integer,
    "username": fields.String,
}


post_fields = {
    "id": fields.Integer,
    "user": fields.Nested(user_fields),
    "title": fields.String,
    "body": fields.String,
    "like_count": fields.Integer,
    "edited_at": fields.DateTime(dt_format="iso8601"),
    "posted_at": fields.DateTime(dt_format="iso8601", attribute="created_at"),
}

analytics_fields = {
    "day": DateField,
    "likes": fields.Integer,
}


class PostResource(Resource):
    @jwt_required()
    @marshal_with(post_fields)
    def post(self):
        parser = post_parser
        data = post_parser.parse_args(strict=True)
        data.update(user=current_user)
        post = Post.create(**data)

        return post

    @jwt_required()
    @paginated_response(post_fields)
    def get(self):
        posts = Post.select()

        return posts


class PostDetailResource(Resource):
    @jwt_required()
    @marshal_with(post_fields)
    def get(self, post_id):
        post = get_or_404(Post, id=post_id)

        return post

    @jwt_required()
    @marshal_with(post_fields)
    def put(self, post_id):
        parser = post_parser
        data = post_parser.parse_args(strict=True)
        post = get_or_404(Post, id=post_id, user=current_user)

        post.title, post.body = data["title"], data["body"]
        post.edited_at = datetime.datetime.utcnow()
        post.save()

        return post

    @jwt_required()
    def delete(self, post_id):
        post = get_or_404(Post, id=post_id, user=current_user)
        post.delete_instance(recursive=True)

        return "", 204


class PostLikeResource(Resource):
    @jwt_required()
    @marshal_with(post_fields)
    def post(self, post_id):
        post = get_or_404(Post, id=post_id)
        post.like(current_user)

        return post

    @jwt_required()
    @marshal_with(post_fields)
    def delete(self, post_id):
        post = get_or_404(Post, id=post_id)
        post.unlike(current_user)

        return post


class PostLikedUsersResource(Resource):
    @jwt_required()
    @paginated_response(user_fields)
    def get(self, post_id):
        post = get_or_404(Post, id=post_id)
        liked_users = post.liked_users

        return liked_users


class PostAnalyticsResource(Resource):
    @jwt_required()
    @marshal_with(analytics_fields)
    def get(self):
        parser = analytics_parser
        dates = parser.parse_args(strict=True)
        date_from, date_to = dates["date_from"], dates["date_to"]
        like_counts = PostLike.daily_likes(date_from, date_to)

        return like_counts
