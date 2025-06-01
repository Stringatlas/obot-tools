import os
import logging
import sys
from datetime import datetime, timezone

def timestamp_to_time(timestamp: int):
    utc_time = datetime.fromtimestamp(timestamp, tz=timezone.utc)
    local_time = utc_time.astimezone()

    return local_time.strftime("%Y-%m-%d %H:%M:%S")

def setup_logger(name):
    """Setup a logger that writes to sys.stderr. This will eventually show up in GPTScript's debugging logs.

    Args:
        name (str): The name of the logger.

    Returns:
        logging.Logger: The logger.
    """
    # Create a logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Set the logging level

    # Create a stream handler that writes to sys.stderr
    stderr_handler = logging.StreamHandler(sys.stderr)

    # Create a log formatter
    formatter = logging.Formatter(
        "[Reddit Tool Debugging Log]: %(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    stderr_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(stderr_handler)

    return logger


logger = setup_logger(__name__)


class ToolRegistry:
    def __init__(self):
        self._tools = {}

    def register(self, name, func):
        """
        Registers a tools by the given 'name'.
        Raises a ValueError if a tools with the same name is already registered.
        """
        if name in self._tools:
            raise ValueError(f"Tool '{name}' is already registered.")
        self._tools[name] = func

    def get(self, name):
        """
        Retrieves a registered tools by name.
        Raises a ValueError if the tools is not found.
        """
        if name not in self._tools:
            raise ValueError(f"Tool '{name}' not found.")
        return self._tools[name]

    def list_tools(self):
        """
        Returns a list of all registered tools names.
        """
        return list(self._tools.keys())

    def decorator(self, name):
        """
        A decorator that automatically registers the decorated function
        under the specified 'name' in the ToolRegistry.
        """

        def wrapper(func):
            self.register(name, func)
            return func

        return wrapper


tool_registry = ToolRegistry()
