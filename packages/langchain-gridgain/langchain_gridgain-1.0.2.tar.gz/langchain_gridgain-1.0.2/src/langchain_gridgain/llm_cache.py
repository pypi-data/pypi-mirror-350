from __future__ import annotations

import hashlib
import json
import logging
from typing import Any, Dict, List, Union, Optional, Tuple
from langchain_core.documents.base import Document
from pyignite import Client as PyigniteClient
from pygridgain import Client as PygridgainClient
from langchain_core.caches import RETURN_VAL_TYPE, BaseCache
from langchain_core.language_models.llms import get_prompts, aget_prompts
from langchain_core.load.dump import dumps
from langchain_core.load.load import loads
from langchain_core.outputs import Generation
from langchain_core.language_models import LLM
from langchain_core.embeddings import Embeddings
from typing_extensions import override
import requests
from langchain_gridgain.vectorstores import GridGainVectorStore


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

GRIDGAIN_SEMANTIC_CACHE_DEFAULT_THRESHOLD = 0.85
GRIDGAIN_SEMANTIC_CACHE_EMBEDDING_CACHE_SIZE = 16

def _hash(_input: str) -> str:
    """Use a deterministic hashing approach."""
    return hashlib.md5(_input.encode()).hexdigest()  # noqa: S324

def _dumps_generations(generations: RETURN_VAL_TYPE) -> str:
    """
    Serialization for generic RETURN_VAL_TYPE, i.e. sequence of `Generation`.

    Args:
        generations (RETURN_VAL_TYPE): A list of language model generations.

    Returns:
        str: A single string representing a list of generations.
    """
    return json.dumps([dumps(_item) for _item in generations])

def _loads_generations(generations_str: str) -> RETURN_VAL_TYPE | None:
    """
    Get Generations from a string.

    Args:
        generations_str (str): A string representing a list of generations.

    Returns:
        RETURN_VAL_TYPE | None: A list of generations or None if parsing fails.
    """
    try:
        return [loads(_item_str) for _item_str in json.loads(generations_str)]
    except (json.JSONDecodeError, TypeError):
        try:
            gen_dicts = json.loads(generations_str)
        except (json.JSONDecodeError, TypeError):
            logger.warning(f"Malformed/unparsable cached blob encountered: '{generations_str}'")
            return None
        else:
            generations = [Generation(**generation_dict) for generation_dict in gen_dicts]
            logger.warning(f"Legacy 'Generation' cached blob encountered: '{generations_str}'")
            return generations

class GridGainCache(BaseCache):
    """Cache that uses GridGain/Apache Ignite as a backend."""

    def __init__(
        self,
        cache_name: str,
        client: Union[PyigniteClient, PygridgainClient] = None,
    ) -> None:
        """
        Initialize the GridGainCache.

        Args:
            cache_name (str): Name of the GridGain cache to use.
            client (Union[PyigniteClient, PygridgainClient]): Pre-configured GridGain or Apache Ignite client.

        Raises:
            Exception: If cache creation or retrieval fails.
        """
        self.cache_name = cache_name
        self.client = client
        try:
            self.cache = self.client.get_or_create_cache(self.cache_name)
            logger.info(f"Cache '{cache_name}' created or retrieved successfully")
        except Exception as e:
            logger.exception(f"Failed to create or retrieve cache '{cache_name}': {e}")
            raise

    @staticmethod
    def _make_id(prompt: str, llm_string: str) -> str:
        """
        Create a unique identifier for a prompt-llm pair.

        Args:
            prompt (str): The input prompt.
            llm_string (str): A string representation of the LLM.

        Returns:
            str: A unique identifier.
        """
        
        # Hash the extracted and normalized user query
        normalized_prompt = prompt.strip().lower()
        return _hash(normalized_prompt)
    
    @override
    def lookup(self, prompt: str, llm_string: str) -> RETURN_VAL_TYPE | None:
        """
        Retrieve cached generations for a given prompt and LLM.

        Args:
            prompt (str): The input prompt.
            llm_string (str): A string representation of the LLM.

        Returns:
            RETURN_VAL_TYPE | None: The cached generations if found, else None.

        Raises:
            Exception: If retrieval from the cache fails.
        """
        try:
            doc_id = self._make_id(prompt, llm_string)
            item = self.cache.get(doc_id)
            if item is not None:
                logging.info("cache hit!!!")
                return _loads_generations(item) 
            else:
                logging.info("cache miss!!!") 
                return None
        except Exception as e:
            logger.exception(f"Failed to lookup cache entry: {e}")
            raise

    @override
    def update(self, prompt: str, llm_string: str, return_val: RETURN_VAL_TYPE) -> None:
        """
        Update the cache with new generations.

        Args:
            prompt (str): The input prompt.
            llm_string (str): A string representation of the LLM.
            return_val (RETURN_VAL_TYPE): The generations to cache.

        Raises:
            Exception: If updating the cache fails.
        """
        try:
            doc_id = self._make_id(prompt, llm_string)
            blob = _dumps_generations(return_val)
            self.cache.put(doc_id, blob)
            logger.info(f"Successfully updated cache for key: {doc_id}")
        except Exception as e:
            logger.exception(f"Failed to update cache: {e}")
            raise

    def delete(self, prompt: str, llm_string: str) -> None:
        """
        Delete a cache entry.

        Args:
            prompt (str): The input prompt.
            llm_string (str): A string representation of the LLM.

        Raises:
            Exception: If deletion from the cache fails.
        """
        try:
            doc_id = self._make_id(prompt, llm_string)
            self.cache.remove_key(doc_id)
            logger.info(f"Successfully deleted cache entry for key: {doc_id}")
        except Exception as e:
            logger.exception(f"Failed to delete cache entry: {e}")
            raise

    def clear(self, **kwargs: Any) -> None:
        """
        Clear all entries from the cache.

        Raises:
            Exception: If clearing the cache fails.
        """
        try:
            self.cache.clear()
            logger.info(f"Successfully cleared all entries from cache: {self.cache_name}")
        except Exception as e:
            logger.exception(f"Failed to clear cache: {e}")
            raise

    def delete_through_llm(
        self, prompt: str, llm: LLM, stop: list[str] | None = None
    ) -> None:
        """
        Delete a cache entry using an LLM object.

        Args:
            prompt (str): The input prompt.
            llm (LLM): The LLM object.
            stop (list[str] | None): Optional stop words for the LLM.

        Raises:
            Exception: If deletion from the cache fails.
        """
        try:
            llm_string = get_prompts(
                {**llm.dict(), "stop": stop},
                [],
            )[1]
            self.delete(prompt, llm_string=llm_string)
        except Exception as e:
            logger.exception(f"Failed to delete cache entry through LLM: {e}")
            raise

    def __del__(self):
        """
        Destructor when the object is destroyed.
        Since the connection is being passed, it's not being closed here.
        """
        logger.info("GridGainCache instance destroyed")

class GridGainSemanticCache(BaseCache):
    def __init__(
        self,
        llm_cache: GridGainCache,
        cache_name: str,
        client: PyigniteClient | PygridgainClient,
        embedding: Embeddings,
        similarity_threshold: float = GRIDGAIN_SEMANTIC_CACHE_DEFAULT_THRESHOLD,
    ):
        self.llm_cache = llm_cache
        self.cache_name = cache_name
        self.client = client
        self.embedding = embedding
        self.similarity_threshold = similarity_threshold
        self.vector_store: GridGainVectorStore = GridGainVectorStore(
            cache_name=cache_name,
            embedding=embedding,
            client=client
        )

    @staticmethod
    def _make_id(prompt: str, llm_string: str) -> str:
        return f"{_hash(prompt)}#{_hash(llm_string)}"

    def _get_embedding(self, text: str) -> List[float]:
        return self.embedding.embed_query(text=text)

    async def _aget_embedding(self, text: str) -> List[float]:
        return await self.embedding.aembed_query(text=text)

    def _extract_user_query(self, prompt: str) -> str:
        start_marker = "user query:"
        end_marker = "\n"
        prompt = prompt.lower()
        start_index = prompt.rfind(start_marker)
        if start_index != -1:
            start_index += len(start_marker)
            end_index = prompt.find(end_marker, start_index)
            if end_index != -1:
                user_query = prompt[start_index:end_index].strip()
            else:
                user_query = prompt[start_index:].strip()
        else:
            user_query = prompt
        return user_query

    def _add_to_vector_cache(self, prompt: str, llm_string: str, return_val: RETURN_VAL_TYPE) -> None:
        user_query: str = self._extract_user_query(prompt)
        doc_id: str = self.llm_cache._make_id(user_query, llm_string)
        texts: List[str]=[user_query]
        print(f"doc_id (id) is {doc_id}")
        print(f"texts (user_query) is {user_query}")

        metadatas: List[Dict[str, str]] = [{"id":doc_id}]
        try:
            self.vector_store.add_texts(texts=texts,metadatas=metadatas)
            self.llm_cache.update(user_query, llm_string, return_val)
        except Exception as e:
            logger.exception(f"Error adding prompt to semantic llm cache : {str(e)}")

    def _query_vector_cache(self, prompt: str) -> Optional[Tuple[str, RETURN_VAL_TYPE]]:
        user_query: str = self._extract_user_query(prompt)
        logger.info(f"Querying semantic cache with user query: {user_query}")
        try:
            documents: List[Document]= self.vector_store.similarity_search(query=user_query,k=1,score_threshold=self.similarity_threshold)
            logger.info(f"the result is {documents}")
            if len(documents) > 0:
                cached_user_query: str = documents[0].page_content
                return self.llm_cache.lookup(prompt=cached_user_query, llm_string=None)
            else:
                return None
        except Exception as e:
            logger.exception(f"Error getting semantic llm cache results: {str(e)}")
            return None
        

    @override
    def update(self, prompt: str, llm_string: str, return_val: RETURN_VAL_TYPE) -> None:
        try:
            self._add_to_vector_cache(prompt, llm_string, return_val)
            logger.info(f"Successfully updated semantic cache for prompt: {prompt}")
        except Exception as e:
            logger.exception(f"Failed to update semantic cache: {e}")
            raise

    @override
    def lookup(self, prompt: str, llm_string: str) -> RETURN_VAL_TYPE | None:
        try:
            user_query = self._extract_user_query(prompt)
            logger.info(f"Looking up semantic cache with user query: {user_query}")
            result: Tuple[str | RETURN_VAL_TYPE[Generation]] | None = self._query_vector_cache(prompt)
            print(f"generations are {result}")
            if result is None:
                logger.info("Semantic cache miss")
                return None
            
            logger.info(f"Semantic cache hit for user query: {user_query}")
            return result
        except Exception as e:
            logger.exception(f"Failed to lookup semantic cache entry: {e}")
            raise

    @override
    async def alookup(self, prompt: str, llm_string: str) -> RETURN_VAL_TYPE | None:
        # For simplicity, we're using the synchronous version here.
        # You can implement an asynchronous version if needed.
        return self.lookup(prompt, llm_string)

    def delete(self, prompt: str, llm_string: str) -> None:
        # Note: The current VectorController doesn't provide a delete endpoint.
        # You might need to implement this on the Java side if needed.
        logger.warning("Delete operation is not supported in the current implementation")

    def clear(self, **kwargs: Any) -> None:
        try:
            response = requests.delete(f"{self.api_endpoint}/api/vector/clear/{self.cache_name}")
            self.llm_cache.clear()
            if response.status_code != 200:
                logger.error(f"Failed to clear semantic cache: {response.text}")
                raise Exception("Failed to clear semantic cache")
            logger.info(f"Successfully cleared all entries from semantic cache: {self.cache_name}")
        except Exception as e:
            logger.exception(f"Failed to clear semantic cache: {e}")
            raise

    def delete_through_llm(self, prompt: str, llm: LLM, stop: list[str] | None = None) -> None:
        llm_string = get_prompts({**llm.dict(), "stop": stop}, [])[1]
        self.delete(prompt, llm_string=llm_string)

    async def adelete_through_llm(self, prompt: str, llm: LLM, stop: list[str] | None = None) -> None:
        llm_string = (await aget_prompts({**llm.dict(), "stop": stop}, []))[1]
        self.delete(prompt, llm_string=llm_string)
