"""
GridGain/Apache Ignite integration for LangChain's BaseStore.
This module provides a GridGainStore class that implements the BaseStore interface,
allowing for seamless integration with LangChain's storage capabilities.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Union, Optional, Sequence, Tuple, Iterator

from langchain_core.stores import BaseStore
from pyignite import Client as PyigniteClient
from pygridgain import Client as PygridgainClient


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GridGainStore(BaseStore[str, str]):
    """
    A storage class that uses GridGain/Apache Ignite as the backend.
    Implements the BaseStore interface from LangChain.
    """

    def __init__(
        self,
        cache_name: str,
        client: Union[PyigniteClient, PygridgainClient]
    ) -> None:
        """
        Initialize the GridGainStore.

        Args:
            cache_name (str): Name of the cache to use in GridGain.
            client (Union[PyigniteClient, PygridgainClient]): Pre-configured Ignite or GridGain client.

        Raises:
            Exception: If cache creation or retrieval fails.
        """
        self.client = client

        try:
            self.cache = self.client.get_or_create_cache(cache_name)
            logger.info(f"Cache '{cache_name}' created or retrieved successfully")
        except Exception as e:
            logger.exception(f"Failed to create or retrieve cache '{cache_name}': {e}")
            raise

    def mget(self, keys: Sequence[str]) -> List[Optional[str]]:
        """
        Retrieve multiple values from the store.

        Args:
            keys (Sequence[str]): A sequence of keys to retrieve.

        Returns:
            List[Optional[str]]: A list of values corresponding to the keys.

        Raises:
            Exception: If retrieval from the cache fails.
        """
        try:
            return [self.cache.get(key) for key in keys]
        except Exception as e:
            logger.exception(f"Failed to retrieve values for keys {keys}: {e}")
            raise

    def mset(self, key_value_pairs: Sequence[Tuple[str, str]]) -> None:
        """
        Set multiple key-value pairs in the store.

        Args:
            key_value_pairs (Sequence[Tuple[str, str]]): A sequence of (key, value) pairs to set.

        Raises:
            Exception: If setting values in the cache fails.
        """
        try:
            for k, v in key_value_pairs:
                self.cache.put(k, v)
            logger.info(f"Successfully set {len(key_value_pairs)} key-value pairs")
        except Exception as e:
            logger.exception(f"Failed to set key-value pairs: {e}")
            raise

    def mdelete(self, keys: Sequence[str]) -> None:
        """
        Delete multiple keys from the store.

        Args:
            keys (Sequence[str]): A sequence of keys to delete.

        Raises:
            Exception: If deletion from the cache fails.
        """
        try:
            for key in keys:
                self.cache.remove_key(key)
            logger.info(f"Successfully deleted {len(keys)} keys")
        except Exception as e:
            logger.exception(f"Failed to delete keys {keys}: {e}")
            raise

    def yield_keys(self, prefix: Optional[str] = None) -> Iterator[str]:
        """
        Yield keys from the store, optionally filtered by a prefix.

        Args:
            prefix (Optional[str]): If provided, only yield keys starting with this prefix.

        Yields:
            str: Keys from the store.

        Raises:
            Exception: If scanning the cache fails.
        """
        try:
            for entry in self.cache.scan():
                key = entry.key
                if not prefix or key.startswith(prefix):
                    yield key
        except Exception as e:
            logger.exception(f"Failed to scan cache: {e}")
            raise

    def __del__(self):
        """
        Destructor when the object is destroyed.
        Since all connections are being passed, none are being closed here.
        """
        logger.info("GridGainStore instance destroyed")