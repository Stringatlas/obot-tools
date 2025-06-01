from tools.helper import tool_registry
from praw.models import Message


def extract_message_content(message: Message) -> dict:
    return {
        "id": message.id,
        "name": message.name,
        "subject": message.subject,
        "body": message.body,
        "body_html": message.body_html,
        "author": str(message.author) if message.author else None,
        "dest": str(message.dest) if message.dest else None,
        "created_utc": message.created_utc,
        "was_comment": message.was_comment,
        "parent_id": message.parent_id if hasattr(message, 'parent_id') else None,
    }



@tool_registry.decorator("GetUnreadMessages")
def get_unread_messages():
    ...