import os
import sys
import praw
from tools.helper import tool_registry

def create_client():
    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    username = os.getenv("REDDIT_USERNAME")
    password = os.getenv("REDDIT_PASSWORD")
    user_agent = "obot:reddit-tools:v1 by (/u/No_Initiative_7898)"

    if username and password:
        return praw.Reddit(
                client_id=client_id,
                client_secret=client_secret,
                user_agent=user_agent,
                username=username,
                password=password)

    return praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent)


@tool_registry.decorator("ValidateCredential")
def validate_credential():
    reddit = create_client()

    try:
        reddit.subreddit("python").hot(limit=1)
        print("Reddit client is valid.")
        sys.exit(0)
    except Exception as e:
        print(f"Reddit client is invalid: {e}")
        sys.exit(1)

read_only_client = create_client()
user_client = create_client()

