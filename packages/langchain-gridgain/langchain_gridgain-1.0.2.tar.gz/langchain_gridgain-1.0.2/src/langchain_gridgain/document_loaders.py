"""
GridGain/Apache Ignite Document Loader for LangChain.
"""
from typing import Any, Dict, List, Optional, Union
import logging

from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document

from pyignite import Client as PyigniteClient
from pygridgain import Client as PygridgainClient

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GridGainDocumentLoader(BaseLoader):
    """Load documents from Ignite / GridGain cache."""

    def __init__(
        self,
        cache_name: str,
        client: Union[PyigniteClient, PygridgainClient],
        filter_criteria: Optional[Dict[str, Any]] = None,
        limit: Optional[int] = None,
        create_cache_if_not_exists: bool = True
    ) -> None:
        """
        Initialize the IgniteDocumentLoader.

        Args:
            cache_name (str): Name of the Ignite cache to use.
            client (Union[PyigniteClient, PygridgainClient]): Pre-configured Ignite or GridGain client.
            filter_criteria (Optional[Dict[str, Any]]): Criteria to filter documents (simple equality checks only).
            limit (Optional[int]): A maximum number of documents to return in the read query.
            create_cache_if_not_exists (bool): If True, create the cache if it doesn't exist.

        Raises:
            Exception: If cache creation or retrieval fails.
        """
        
        self.cache_name = cache_name
        self.filter = filter_criteria
        self.limit = limit
        self.create_cache_if_not_exists = create_cache_if_not_exists
        self.client = client
        try:
            self.cache = self.client.get_or_create_cache(self.cache_name)
        except Exception as e:
            logger.exception(f"Failed to get or create cache: {e}")
            raise

    def list_caches(self) -> List[str]:
        """
        List all available caches in the Ignite cluster.

        Returns:
            List[str]: A list of cache names.

        Raises:
            Exception: If connection to Ignite server fails.
        """
        try:
            return self.client.get_cache_names()
        except Exception as e:
            logger.exception(f"Failed to connect to Ignite server: {e}")
            raise
    
    def populate_cache(self, reviews):
        """
        Populate the cache with sample items.

        Args:
            reviews: A dictionary of sample reviews to populate the cache with.

        Raises:
            Exception: If populating the cache fails.
        """
        try:
            cache = self.client.get_or_create_cache(self.cache_name)
            for laptop_name, review_text in reviews.items():
                cache.put(laptop_name, review_text)
            logger.info(f"Populated cache '{self.cache_name}' with sample items.")
        except Exception as e:
            logger.exception(f"Failed to populate cache: {e}")
            raise
    
    def get(self, key):
        """
        Retrieve a value from the cache by key.

        Args:
            key: The key to retrieve the value for.

        Returns:
            The value associated with the given key.

        Raises:
            Exception: If retrieving the value from the cache fails.
        """
        try:
            cache = self.client.get_or_create_cache(self.cache_name)
            return cache.get(key)
        except Exception as e:
            logger.exception(f"Failed to get value from cache: {e}")
            raise

    def _matches_filter(self, value: Any) -> bool:
        """
        Check if a value matches the filter criteria.
        
        Args:
            value (Any): The value to check against the filter criteria.
        
        Returns:
            bool: True if the value matches the filter, False otherwise.
        """
        if not self.filter:
            return True
        
        if isinstance(value, list):
            return all(self.filter.get(str(i)) == v for i, v in enumerate(value) if str(i) in self.filter)
        elif isinstance(value, dict):
            return all(value.get(k) == v for k, v in self.filter.items())
        elif isinstance(value, (str, int, float, bool)):
            # For simple types, check if any filter value matches the entire value
            return any(v == value for v in self.filter.values())
        else:
            # For other types (e.g., custom objects), convert to string and check
            str_value = str(value)
            return any(v == str_value for v in self.filter.values())

    def load(self) -> List[Document]:
        """
        Load data into Document objects.

        Returns:
            List[Document]: A list of Document objects loaded from the cache.

        Raises:
            Exception: If loading documents fails.
        """
        documents = []
        try:
            cache = self.client.get_cache(self.cache_name)
            for key, value in cache.scan():
                documents.append(Document(
                    page_content=str(value),
                    metadata={"key": key, "cache": self.cache_name}
                ))
                if self.limit and len(documents) >= self.limit:
                    break

            return documents

        except Exception as e:
            logger.exception(f"Failed to load documents: {e}")
            logger.info("Available caches: %s", ", ".join(self.client.get_cache_names()))
            raise

    def __del__(self):
        """
        Destructor when the object is destroyed.
        Since all connections are being passed, none are being closed here.
        """
        logger.info("GridGainStore instance destroyed")