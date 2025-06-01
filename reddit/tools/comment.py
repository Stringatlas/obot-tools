from praw.models import Comment
from tools.helper import timestamp_to_time

def extract_comment_attributes(comment: Comment):
    return {
        'id': comment.id,
        'author': str(comment.author) if comment.author else None,
        'body': comment.body,
        'created_time': timestamp_to_time(comment.created_utc),
        'score': comment.score,
        'subreddit': str(comment.subreddit),
        'submission_id': comment.link_id,
        'parent_id': comment.parent_id,
        'permalink': comment.permalink,
        'is_submitter': comment.is_submitter,
        'distinguished': comment.distinguished,
        'edited': comment.edited,
        'stickied': comment.stickied,
        'saved': comment.saved
    }
