import os
from tools.helper import tool_registry
from tools.reddit import read_only_client
from praw.models import ListingGenerator, Submission
from tools.comment import extract_comment_attributes


def extract_submission_attributes(submission: Submission):
    """
    Extracts relevant attributes from a Reddit Submission object into a dictionary.
    """
    data = {
        'id': submission.id,
        'title': submission.title,
        'author': submission.author.name if submission.author else None,
        'subreddit': submission.subreddit.display_name,
        'score': submission.score,
        'upvote_ratio': submission.upvote_ratio,
        'num_comments': submission.num_comments,
        'created_utc': submission.created_utc,
        'url': submission.url,
        'permalink': submission.permalink,
        'selftext': submission.selftext,
        'is_spoiler': submission.spoiler,
        'is_locked': submission.locked,
        'is_stickied': submission.stickied,
    }

    if hasattr(submission, 'poll_data') and submission.poll_data:
        data['poll'] = {
            'total_vote_count': submission.poll_data.total_vote_count,
            'user_selection': submission.poll_data.user_selection,
            'voting_end_timestamp': submission.poll_data.voting_end_timestamp,
            'options': [
                dict(
                    id=option.id,
                    text=option.text,
                    **({'vote_count': option.vote_count} if hasattr(option, 'vote_count') else {})
                )
                for option in submission.poll_data.options
            ]
        }

    if hasattr(submission, 'gallery_data') and submission.gallery_data:
        items = submission.gallery_data['items']
        media_metadata = submission.media_metadata
        gallery = []
        for item in items:
            media_id = item['media_id']
            meta = media_metadata.get(media_id, {})
            if meta.get('e') == 'Image':
                source = meta.get('s', {})
                gallery.append({
                    'url': source.get('u'),
                    'width': source.get('x'),
                    'height': source.get('y'),
                    'caption': item.get('caption')
                })
        data['gallery'] = gallery

    if hasattr(submission, 'media') and submission.media:
        reddit_video = submission.media.get('reddit_video')
        if reddit_video:
            data['video'] = {
                'fallback_url': reddit_video.get('fallback_url'),
                'height': reddit_video.get('height'),
                'width': reddit_video.get('width'),
                'duration': reddit_video.get('duration')
            }

    return data


def fetch_submissions(listing_generator: ListingGenerator):
    """
    Converts generator object returned by API to a list of objects
    """
    posts = []

    for post in listing_generator:
        posts.append(extract_submission_attributes(post))
        print("found post: " + post.title)

    return posts


@tool_registry.decorator("SearchRedditPosts")
def search_reddit_posts():
    """
    Searches Reddit posts based on a keyword in a specified subreddit.
    """
    subreddit = os.getenv("SUBREDDIT") or "all"
    keyword = os.getenv("KEYWORD")
    limit = int(os.getenv("LIMIT") or 10)

    return fetch_submissions(read_only_client.subreddit(subreddit).search(keyword, limit=limit))


@tool_registry.decorator("GetPosts")
def get_posts():
    """
    Fetches Reddit posts from a specified subreddit using sorting, time filter, and limit.
    """
    subreddit = os.getenv("SUBREDDIT") or "all"
    sort_by = os.getenv("SORT_BY") or "top"
    time_filter = os.getenv("TIME_FILTER") or "all"
    limit = int(os.getenv("LIMIT") or 10)

    match sort_by:
        case "top":
            results = read_only_client.subreddit(subreddit).top(limit=limit)
        case "hot":
            results = read_only_client.subreddit(subreddit).hot(limit=limit, time_filter=time_filter)
        case "new":
            results = read_only_client.subreddit(subreddit).new(limit=limit)
        case "rising":
            results = read_only_client.subreddit(subreddit).rising(limit=limit)
        case "controversial":
            results = read_only_client.subreddit(subreddit).controversial(limit=limit, time_filter=time_filter)
        case _:
            print(f"Invalid sort_by value: {sort_by}")
            return {}

    return fetch_submissions(results)


@tool_registry.decorator("GetCommentsOnPost")
def get_comments_on_post():
    """
    Fetches extracted comment attributes for all top-level comments on a reddit post.
    """
    post_id = os.getenv("POST_ID")
    limit = int(os.getenv("LIMIT") or 10)

    submission = read_only_client.submission(id=post_id)
    submission.comments.replace_more(limit=None)
    return [extract_comment_attributes(comment) for comment in submission.comments.list()]


@tool_registry.decorator("GetPostFromID")
def get_post_from_id():
    post_id = os.getenv("POST_ID")

    return extract_submission_attributes(read_only_client.submission(id=post_id))
