import os
from tools.helper import tool_registry
from praw.models import Message
from tools.reddit import user_client


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
    """
    Retrieves unread messages from the user's Reddit inbox and optionally marks them as read.
    """
    mark_read = os.getenv("MARK_READ", "No").lower() == "yes"
    unread = user_client.inbox.unread()

    return [(lambda m: m.mark_read() or extract_message_content(m) if mark_read 
            else extract_message_content(m))(message) for message in unread]


@tool_registry.decorator("GetRecentMessages")
def get_recent_messages():
    limit = int(os.getenv("LIMIT") or 10)
    messages = user_client.inbox.messages(limit=limit)

    return [extract_message_content(message) for message in messages]


@tool_registry.decorator("GetInboxItems")
def get_inbox_items():
    limit = int(os.getenv("LIMIT") or 10)
    messages = user_client.inbox.all(limit=limit)

    return [extract_message_content(messages) for messages in messages]