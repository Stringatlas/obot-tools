import os
from tools.helper import tool_registry, timestamp_to_time
from tools.reddit import read_only_client, user_client

from praw.models import Redditor
from tools.post import extract_submission_attributes
from tools.comment import extract_comment_attributes


def extract_user_profile(user: Redditor):
    return {
        "name": user.name,
        "id": user.id,
        "icon_img": getattr(user, "icon_img", None),
        "created_utc": timestamp_to_time(user.created_utc),
        "is_employee": user.is_employee,
        "is_mod": user.is_mod,
        "is_gold": user.is_gold,
        "link_karma": user.link_karma,
        "comment_karma": user.comment_karma,
        "total_karma": getattr(user, "total_karma", user.link_karma + user.comment_karma),
        "has_verified_email": getattr(user, "has_verified_email", None),
        "accept_followers": getattr(user, "accept_followers", None),
        "subreddit": user.subreddit.display_name if getattr(user, "subreddit", None) else None
    }

@tool_registry.decorator("GetUserProfile")
def get_user_profile():
    username = os.getenv("USERNAME")
    user: Redditor = read_only_client.redditor(name=username)

    return extract_user_profile(user)


@tool_registry.decorator("GetUserComments")
def get_user_comments():
    username = os.getenv("USERNAME")
    limit = os.getenv("LIMIT")
    user: Redditor = read_only_client.redditor(username)

    return [extract_comment_attributes(comment) for comment in user.comments.new(limit=limit)]


@tool_registry.decorator("GetUserPosts")
def get_user_posts():
    username = os.getenv("USERNAME")
    limit = os.getenv("LIMIT")
    user: Redditor = read_only_client.redditor(username)

    return [extract_submission_attributes(post) for post in user.submissions.new(limit=limit)]

@tool_registry.decorator("GetMyProfile")
def get_my_profile():
    me = user_client.user.me()

    return extract_user_profile(me)


