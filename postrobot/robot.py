import json
import random

import requests
import urllib.parse
from faker import Faker


POSTBOOK_HOST = "http://localhost:5000"


class RobotException(Exception):
    pass


class RobotRequestError(Exception):
    pass


class RobotBadResponse(RobotException):
    pass


def _make_request(method, endpoint, **kwargs):
    url = urllib.parse.urljoin(POSTBOOK_HOST, endpoint)

    try:
        resp = requests.request(method, url, **kwargs)
    except requests.RequestException as e:
        raise RobotRequestError from e
    else:
        if not resp.ok:
            msg = f"Bad response from {url}: {resp.status_code} {resp.text}"
            raise RobotBadResponse(msg)

        return resp


def _auth_header(token):
    return {"Authorization": f"Bearer {token}"}


def register_user(username, password):
    payload = {"username": username, "password": password}
    resp = _make_request("POST", "/auth/register/", json=payload)

    return resp.json()["access_token"]


def login_user(username, password):
    payload = {"username": username, "password": password}
    resp = _make_request("POST", "/auth/login/", json=payload)

    return resp.json()["access_token"]


def create_post(title, body, access_token):
    payload = {"title": title, "body": body}
    headers = _auth_header(access_token)
    resp = _make_request("POST", "/posts/", json=payload, headers=headers)

    return resp.json()["id"]


def like_post(post_id, access_token):
    headers = _auth_header(access_token)
    resp = _make_request("POST", f"/posts/{post_id}/like/", headers=headers)

    return resp.json()["id"]


class Robot:
    DEFAULT_USER_COUNT = 10
    DEFAULT_POST_COUNT = 15
    DEFAULT_LIKE_COUNT = 20

    def __init__(
        self,
        user_count=DEFAULT_USER_COUNT,
        post_count=DEFAULT_POST_COUNT,
        like_count=DEFAULT_LIKE_COUNT,
    ):
        self.user_count = user_count
        self.post_count = post_count
        self.like_count = like_count

        self.access_tokens = []
        self.post_ids = []
        self.faker = Faker()

    def start(self):
        self.create_users()
        self.create_posts()
        self.like_posts()

    def create_users(self):
        for _ in range(self.user_count):
            user_email = self.faker.email()
            user_password = self.faker.pystr(min_chars=15, max_chars=25)
            access_token = register_user(user_email, user_password)
            self.access_tokens.append(access_token)

    def create_posts(self):
        for access_token in self.access_tokens:
            for _ in range(self.post_count):
                title = self.faker.sentence()
                body = self.faker.paragraph(20)
                post_id = create_post(title, body, access_token)
                self.post_ids.append(post_id)

    def like_posts(self):
        for access_token in self.access_tokens:
            for _ in range(self.like_count):
                post_id = random.choice(self.post_ids)
                liked_post = like_post(post_id, access_token)


def robot_from_conf():
    with open("config.json", "r") as conf_file:
        config = json.load(conf_file)

    user_count = config["user_count"]
    post_count = config["post_count"]
    like_count = config["like_count"]
    robot = Robot(user_count=user_count, post_count=post_count, like_count=like_count)

    return robot


if __name__ == "__main__":
    robot = robot_from_conf()
    robot.start()
