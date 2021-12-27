from .auth import (
    UserRegisterResource,
    UserLoginResource,
    RefreshTokenResource,
    UserActivityResource,
)
from .post import (
    PostResource,
    PostDetailResource,
    PostLikeResource,
    PostLikedUsersResource,
    PostAnalyticsResource,
)


def add_resources(api):
    auth_prefix = "/auth"
    api.add_resource(UserRegisterResource, f"{auth_prefix}/register/")
    api.add_resource(UserLoginResource, f"{auth_prefix}/login/")
    api.add_resource(RefreshTokenResource, f"{auth_prefix}/refresh/")
    api.add_resource(UserActivityResource, f"{auth_prefix}/activity/")

    post_prefix = "/posts"
    api.add_resource(PostResource, f"{post_prefix}/")
    api.add_resource(PostDetailResource, f"{post_prefix}/<int:post_id>/")
    api.add_resource(PostLikeResource, f"{post_prefix}/<int:post_id>/like/")
    api.add_resource(
        PostLikedUsersResource, f"{post_prefix}/<int:post_id>/liked_users/"
    )
    api.add_resource(PostAnalyticsResource, f"{post_prefix}/analytics/")
