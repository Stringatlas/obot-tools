import os
from tools.helper import tool_registry
from tools.reddit import read_only_client
from praw.models import Subreddit


def extract_subreddit_attributes(subreddit: Subreddit):
    """
    Extracts relevant attributes from a Reddit Subreddit object into a dictionary.
    """
    data = {
        'id': subreddit.id,
        'name': subreddit.display_name,
        'title': subreddit.title,
        'description': subreddit.public_description,
        'subscribers': subreddit.subscribers,
        'created_utc': subreddit.created_utc,
        'url': subreddit.url,
        'over18': subreddit.over18,
        'active_user_count': subreddit.active_user_count,
        'icon_img': subreddit.icon_img,
        'banner_img': subreddit.banner_img,
        'header_img': subreddit.header_img,
    }
    
    return data


@tool_registry.decorator("GetSubredditInformation")
def get_subreddit_information():
    """
    Retrieves information about a subreddit by its name.
    """
    subreddit_name = os.getenv("SUBREDDIT")

    subreddit = read_only_client.subreddit(subreddit_name)
    return extract_subreddit_attributes(subreddit)


@tool_registry.decorator("SearchForSubreddit")
def search_for_subreddit():
    """
    Searches for a subreddit
    """
    keyword = os.getenv("KEYWORD")
    limit = int(os.getenv("LIMIT") or 5)
    subreddits = read_only_client.subreddits.search(keyword, limit=limit)
    return [extract_subreddit_attributes(subreddit) for subreddit in subreddits]


@tool_registry.decorator("GetSubreddits")
def get_subreddits():
    """
    Retrieves a list of subreddits based on the specified sort order.
    """
    sort_by = os.getenv("SORT_BY", "default")
    limit = int(os.getenv("LIMIT") or 5)

    match sort_by:
        case "default":
            subreddits = read_only_client.subreddits.default(limit=limit)
        case "popular":
            subreddits = read_only_client.subreddits.popular(limit=limit)
        case "new":
            subreddits = read_only_client.subreddits.new(limit=limit)
        case _:
            raise ValueError(f"Invalid sort_by value: {sort_by}")

    return [extract_subreddit_attributes(subreddit) for subreddit in subreddits]


@tool_registry.decorator("GetTrendingSubreddits")
def get_trending_subreddits():
    """
    Retrieves a list of trending subreddits.
    """
    return [extract_subreddit_attributes(subreddit) for subreddit in read_only_client.subreddits.trending()]
