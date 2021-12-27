import os
from datetime import timedelta

SECRET_KEY = os.environ.get(
    "SECRET_KEY", "0e644f93525abbfcb66278cb1fd5dbc24e32f66eceaf2ca9b4d711ce442b2365"
)

DB_USER = os.environ.get("DB_USER", "postbook")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "postbook")
DB_NAME = os.environ.get("DB_NAME", "postbook")
DB_HOST = os.environ.get("DB_HOST", "127.0.0.1")
DB_PORT = os.environ.get("DB_PORT", "3306")
DB_URI = f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
JWT_SECRET_KEY = os.environ.get(
    "JWT_SECRET_KEY", "a0f33040399fc3457568c295348ce24bdb284289ea812d2ef5f5a066e50d41dc"
)

PROPAGATE_EXCEPTIONS = True
