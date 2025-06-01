from praw.models import Comment
from tools.helper import timestamp_to_time, tool_registry
from tools.reddit import user_client
import os


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


@tool_registry.decorator("CommentOnPost")
def comment_on_post():
    """
    Add a comment to a Reddit post.
    """
    try:
        post_id = os.getenv("POST_ID")
        text = os.getenv("TEXT")
        submission = user_client.submission(id=post_id)
        comment = submission.reply(text)

        comment_data = extract_comment_attributes(comment)

        return {
            "status": "success",
            "comment_data": comment_data
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


@tool_registry.decorator("ReplyComment")
def reply_to_comment():
    """
    Reply to an existing Reddit comment.
    """
    try:
        comment_id = os.getenv("COMMENT_ID")
        text = os.getenv("TEXT")

        parent_comment = user_client.comment(id=comment_id)
        reply = parent_comment.reply(text)

        reply_data = extract_comment_attributes(reply)

        return {
            "status": "success",
            "reply_data": reply_data
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }