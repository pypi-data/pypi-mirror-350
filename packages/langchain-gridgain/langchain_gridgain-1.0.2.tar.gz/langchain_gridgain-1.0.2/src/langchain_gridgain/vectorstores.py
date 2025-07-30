import requests
from typing import Any, Dict, Iterable, List, Optional, Tuple
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStore
from pygridgain import Client, GenericObjectMeta
from pygridgain.datatypes import *
from pygridgain.datatypes.prop_codes import *
from collections import OrderedDict
import logging
import time
from io import BytesIO
from pygridgain.datatypes.cache_config import CacheMode, CacheAtomicityMode, WriteSynchronizationMode, IndexType
from pygridgain.datatypes.prop_codes import PROP_NAME, PROP_CACHE_MODE, PROP_CACHE_ATOMICITY_MODE, \
    PROP_WRITE_SYNCHRONIZATION_MODE, PROP_QUERY_ENTITIES


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Article(metaclass=GenericObjectMeta, 
             type_name='Article',
             schema=OrderedDict([
                 ('content', String),
                 ('contentVector', FloatArrayObject),
             ])):
    pass

def get_cache_config(cache_name):
    return {
        PROP_NAME: cache_name,
        PROP_CACHE_MODE: CacheMode.REPLICATED,
        PROP_CACHE_ATOMICITY_MODE: CacheAtomicityMode.TRANSACTIONAL,
        PROP_WRITE_SYNCHRONIZATION_MODE: WriteSynchronizationMode.FULL_SYNC,
        PROP_QUERY_ENTITIES: [{
            'table_name': cache_name,
            'key_field_name': 'id',
            'key_type_name': 'java.lang.String',
            'value_field_name': None,
            'value_type_name': Article.type_name,
            'field_name_aliases': [],
            'query_fields': [
                {
                    'name': 'id',
                    'type_name': 'java.lang.String'
                },
                {
                    'name': 'content',
                    'type_name': 'java.lang.String'
                },
                {
                    'name': 'contentVector',
                    'type_name': '[F'
                }
            ],
            'query_indexes': [
                {
                    'index_name': 'contentVector',
                    'index_type': IndexType.VECTOR,
                    'inline_size': 1024,
                    'fields': [
                        {
                            'name': 'contentVector'
                        }
                    ]
                }
            ]
        }],
    }

class GridGainVectorStore(VectorStore):
    """
    A vector store implementation using GridGain for storing and querying embeddings.
    """

    def __init__(
        self,
        cache_name: str,
        embedding: Embeddings,
        client: Client,
    ):
        """
        Initialize the GridGainVectorStore.

        Args:
            embedding (Embeddings): The embedding model to use.
            api_endpoint (str): The API endpoint for the GridGain service.
        """
        self.cache_name = cache_name
        self.embedding = embedding
        self.client = client
        try:
            self.cache = self.client.get_or_create_cache(get_cache_config(self.cache_name))
            logger.info(f"Cache '{cache_name}' created or retrieved successfully")
        except Exception as e:
            logger.exception(f"Failed to create or retrieve cache '{cache_name}': {e}")
            raise

    @property
    def embeddings(self) -> Embeddings:
        """
        Get the embedding model used by this vector store.

        Returns:
            Embeddings: The embedding model.
        """
        return self.embedding

    def generate_nanosec_id(self) -> int:
        """Generate a unique ID based on the current timestamp in nanoseconds."""
        return time.time_ns()

    def add_texts(
        self,
        texts: Iterable[str],
        metadatas: Optional[List[dict]] = None,
        ids: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> List[str]:
        """
        Add texts to the vector store one at a time and return the titles.

        Args:
            texts (Iterable[str]): The texts to add.
            metadatas (Optional[List[dict]]): Metadata for each text.
            ids (Optional[List[str]]): IDs for each text (not used in this implementation).
            **kwargs: Additional keyword arguments.

        Returns:
            List[str]: The titles of the added texts.
        """
        embedding_vectors = self.embedding.embed_documents(list(texts))
        
        if metadatas is None:
            metadatas = [{} for _ in texts]

        cache = self.client.get_cache(self.cache_name)
        added_titles = []
        for text, metadata, embedding_vector in zip(texts, metadatas, embedding_vectors):
            id:str = metadata["id"]
            article = Article(content=text,contentVector=embedding_vector)
            cache.put(id, article)
            added_titles.append(id)

        logger.info(f"All articles processed. Added {len(added_titles)} articles.")
        return added_titles
    

    def similarity_search_with_score_by_vector(
        self,
        embedding: List[float],
        k: int = 4,
        filter: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> List[Tuple[Document, float]]:
        """
        Perform a similarity search using a vector.

        Args:
            embedding (List[float]): The query embedding vector.
            k (int): The number of results to return.
            filter (Optional[Dict[str, Any]]): Additional filter criteria (Not used).

        Returns:
            List[Tuple[Document, float]]: List of tuples containing similar documents and their scores.
        """
        documents = []
        print(f"cache is {self.cache_name}")
        cache = self.client.get_cache(self.cache_name)
        score_threshold = kwargs.get("score_threshold")
        cursor = cache.vector(type_name=Article.type_name, field='contentVector', clause_vector=embedding, k=k, threshold=score_threshold)
        results = {k: v for k, v in cursor}
        
        try:
            for key, article in results.items():
                try:
                    doc = Document(
                        page_content=article.content,
                        metadata={
                            "id": key,
                        }
                    )
                    score = 1.0
                    documents.append((doc, score))
                except AttributeError as e:
                    print(f"Error processing article with key {key}: {str(e)}")
                    continue  # Skip this article and continue with the next
        except Exception as e:
            print(f"Error processing results: {str(e)}")
            raise
        
        return documents

    def similarity_search(
        self,
        query: str,
        k: int = 4,
        filter: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> List[Document]:
        """
        Perform a similarity search using a text query.

        Args:
            query (str): The text query.
            k (int): The number of results to return.
            filter (Optional[Dict[str, Any]]): Additional filter criteria.
            **kwargs: Additional keyword arguments.

        Returns:
            List[Document]: List of similar documents.
        """
        logger.info(f"*******similarity_search starts for {query}******")
        query_embedding = self.embedding.embed_query(query)
        score_threshold = kwargs.get("score_threshold")
        docs_and_scores = self.similarity_search_with_score_by_vector(query_embedding, k, filter, score_threshold=score_threshold)
        logger.info(f"*******similarity_search ends for {query}******")

        return [doc for doc, _ in docs_and_scores]

    def clear(self) -> None:
        """
        Clear all documents from the vector store.
        """
        try:
            response = requests.delete(f"{self.api_endpoint}/api/vector/clear/{self.cache_name}")
            if response.status_code != 200:
                logger.error(f"Failed to clear vector cache: {response.text}")
                raise Exception("Failed to clear vector cache")
            logger.info(f"Successfully cleared all entries from vector cache: {self.cache_name}")
        except Exception as e:
            logger.exception(f"Failed to clear vector cache: {e}")
            raise
        response.raise_for_status()

    @classmethod
    def from_texts(
        cls,
        texts: List[str],
        embedding: Embeddings,
        metadatas: Optional[List[dict]] = None,
        ids: Optional[List[str]] = None,
        api_endpoint: str = None,
        **kwargs: Any,
    ) -> 'GridGainVectorStore':
        """
        Create a GridGainVectorStore instance from a list of texts.

        Args:
            texts (List[str]): The texts to add to the vector store.
            embedding (Embeddings): The embedding model to use.
            metadatas (Optional[List[dict]]): Metadata for each text.
            ids (Optional[List[str]]): IDs for each text.
            api_endpoint (str): The API endpoint for the GridGain service.
            **kwargs: Additional keyword arguments.

        Returns:
            GridGainVectorStore: An instance of GridGainVectorStore.

        Raises:
            ValueError: If the API endpoint is not provided.
        """
        if api_endpoint is None:
            raise ValueError("API endpoint must be provided")

        instance = cls(embedding=embedding, api_endpoint=api_endpoint, **kwargs)
        instance.add_texts(texts=texts, metadatas=metadatas, ids=ids)
        return instance

    # Placeholder for async methods
    async def aadd_texts(self, texts: Iterable[str], metadatas: Optional[List[dict]] = None, **kwargs: Any) -> List[str]:
        """
        Asynchronous version of add_texts (not implemented).

        Args:
            texts (Iterable[str]): The texts to add.
            metadatas (Optional[List[dict]]): Metadata for each text.
            **kwargs: Additional keyword arguments.

        Returns:
            List[str]: The IDs of the added texts.
        """
        # Implement async version if needed
        pass

    async def asimilarity_search_with_score_by_vector(self, embedding: List[float], k: int = 4, filter: Optional[Dict[str, Any]] = None) -> List[Tuple[Document, float]]:
        """
        Asynchronous version of similarity_search_with_score_by_vector (not implemented).

        Args:
            embedding (List[float]): The query embedding vector.
            k (int): The number of results to return.
            filter (Optional[Dict[str, Any]]): Additional filter criteria.

        Returns:
            List[Tuple[Document, float]]: List of tuples containing similar documents and their scores.
        """
        # Implement async version if needed
        pass

    def convert_to_float_array(self, embedding):
        """
        Convert a list of floats to FloatArrayObject using BytesIO as the stream.
        
        Args:
            embedding (List[float]): List of float values to convert
            
        Returns:
            FloatArrayObject: The converted float array object
        """
        stream = BytesIO()
        try:
            return FloatArrayObject.from_python_not_null(stream, embedding)
        except Exception as e:
            # Fallback to direct constructor if from_python_not_null fails
            return FloatArrayObject(embedding)