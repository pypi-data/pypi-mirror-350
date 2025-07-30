"""
GridGain/Apache Ignite-based chat message history for LangChain.
"""
from __future__ import annotations

import json
import logging
from typing import List, Union, Sequence
from pyignite import Client as PyigniteClient
from pygridgain import Client as PygridgainClient
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import (
    BaseMessage,
    message_to_dict,
    messages_from_dict,
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DEFAULT_CACHE_NAME = "langchain_message_store"

class GridGainChatMessageHistory(BaseChatMessageHistory):
    """Chat message history that stores history in Apache GridGain."""

    def __init__(
        self,
        *,
        session_id: str,
        cache_name: str = DEFAULT_CACHE_NAME,
        client: Union[PyigniteClient, PygridgainClient]
    ) -> None:
        """
        Initialize the IgniteChatMessageHistory.

        Args:
            session_id (str): Arbitrary key used to store the messages of a single chat session.
            cache_name (str): Name of the cache to create/use. Defaults to DEFAULT_CACHE_NAME.
            client (Union[PyigniteClient, PygridgainClient]): Pre-configured Ignite or GridGain client.

        Raises:
            Exception: If cache creation or retrieval fails.
        """
        self.session_id = session_id
        self.cache_name = cache_name
        self.client = client
        try:
            self.cache = self.client.get_or_create_cache(self.cache_name)
        except Exception as e:
            logger.exception(f"Failed to get or create cache: {e}")
            raise

    @property
    def messages(self) -> List[BaseMessage]:
        """
        Retrieve all session messages from Ignite.

        Returns:
            List[BaseMessage]: A list of all messages in the current session.

        Raises:
            Exception: If message retrieval fails.
        """
        key = f"{self.session_id}_messages"
        try:
            messages_json = self.cache.get(key)
            if not messages_json:
                return []
            items = json.loads(messages_json)
            return messages_from_dict(items)
        except Exception as e:
            logger.exception(f"Failed to retrieve messages: {e}")
            raise

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        """
        Add messages to the cache.

        Args:
            messages (Sequence[BaseMessage]): Sequence of messages to add.

        Raises:
            Exception: If adding messages fails.
        """
        key = f"{self.session_id}_messages"
        try:
            existing_messages = self.messages
            new_messages = existing_messages + list(messages)
            messages_json = json.dumps([message_to_dict(m) for m in new_messages])
            self.cache.put(key, messages_json)
        except Exception as e:
            logger.exception(f"Failed to add messages: {e}")
            raise

    def clear(self) -> None:
        """
        Clear session messages from the Ignite cache.

        Raises:
            Exception: If clearing messages fails.
        """
        key = f"{self.session_id}_messages"
        try:
            self.cache.remove_key(key)
        except Exception as e:
            logger.exception(f"Failed to clear messages: {e}")
            raise

    def __del__(self):
        """
        Destructor when the object is destroyed.
        Since all connections are being passed, none are being closed here.
        """
        logger.info("GridGainChatMessageHistory instance destroyed")