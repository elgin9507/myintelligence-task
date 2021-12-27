import datetime
from collections import Counter
from functools import cached_property

from peewee import Model, DateTimeField, CharField, ForeignKeyField, TextField, fn
from playhouse.db_url import connect

from .config import DB_URI


db = connect(DB_URI)


class BaseModel(Model):
    created_at = DateTimeField(default=datetime.datetime.utcnow, index=True)

    class Meta:
        database = db


class User(BaseModel):
    username = CharField(max_length=255, unique=True)
    password = CharField(max_length=1000)
    last_login_date = DateTimeField(null=True)
    last_activity = DateTimeField(null=True)


class Post(BaseModel):
    user = ForeignKeyField(User, backref="posts")
    title = CharField(max_length=250)
    body = TextField()
    edited_at = DateTimeField(null=True)

    def like(self, user):
        PostLike.get_or_create(user=user, post=self)

    def unlike(self, user):
        PostLike.delete().where(PostLike.user == user, PostLike.post == self).execute()

    @cached_property
    def like_count(self):
        likes = PostLike.select().where(PostLike.post == self)

        return likes.count()

    @cached_property
    def liked_users(self):
        users = User.select().join(PostLike).where(PostLike.post == self.id)

        return users


class PostLike(BaseModel):
    user = ForeignKeyField(User, backref="likes")
    post = ForeignKeyField(Post, backref="likes")

    class Meta:
        indexes = ((("user", "post"), True),)

    @classmethod
    def daily_likes(cls, start_date, end_date):
        likes = cls.select(fn.Date(cls.created_at)).where(
            (cls.created_at >= start_date) & (cls.created_at <= end_date)
        )
        dates = [l.created_at for l in likes]
        counter = Counter(dates)
        like_counts = []

        while start_date <= end_date:
            like_counts.append({"day": start_date, "likes": counter.get(start_date, 0)})
            start_date += datetime.timedelta(days=1)

        return like_counts
