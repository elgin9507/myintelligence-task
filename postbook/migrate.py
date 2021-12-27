from postbook.models import db, User, Post, PostLike

db.create_tables([User, Post, PostLike])
