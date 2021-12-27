import datetime

from flask_jwt_extended import current_user


def update_user_activity(*args, **kwargs):
    user = current_user

    if not user:
        return

    user.last_activity = datetime.datetime.utcnow()
    user.save()
