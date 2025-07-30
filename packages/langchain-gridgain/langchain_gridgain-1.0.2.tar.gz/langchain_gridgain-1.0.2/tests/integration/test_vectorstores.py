import unittest
import logging
from pygridgain import Client
from langchain_core.embeddings import Embeddings
from langchain_core.documents import Document
from langchain_gridgain.vectorstores import GridGainVectorStore, Article
from pygridgain.exceptions import CacheError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VariableEmbeddings(Embeddings):
    """Mock embeddings that return different vectors based on input"""
    def embed_documents(self, texts):
        vectors = {
            "high_similarity": [0.99, 0.99, 0.99, 0.99],
            "medium_similarity": [0.6, 0.6, 0.6, 0.6],
            "low_similarity": [0.1, 0.1, 0.1, 0.1],
            "default": [0.5, 0.5, 0.5, 0.5]
        }
        return [vectors.get(text, vectors["default"]) for text in texts]

    def embed_query(self, text):
        return [0.99, 0.99, 0.99, 0.99]

class TestGridGainVectorStoreIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up GridGain client."""
        try:
            cls.client = Client()
            cls.client.connect('localhost', 10800)
            logger.info("Successfully connected to GridGain server")
            cls.cache_name = "test_vector_cache"
        except Exception as e:
            logger.error(f"Error in setUpClass: {str(e)}")
            raise

    @classmethod
    def tearDownClass(cls):
        """Close the client connection."""
        try:
            cls.client.close()
            logger.info("Closed GridGain connection")
        except Exception as e:
            logger.error(f"Error in tearDownClass: {str(e)}")

    def setUp(self):
        """Set up test environment."""
        self.embeddings = VariableEmbeddings()
        self.vector_store = GridGainVectorStore(
            cache_name=self.cache_name,
            embedding=self.embeddings,
            client=self.client
        )
        # Clear the cache before each test
        self.vector_store.cache.clear()

    def test_similarity_search_with_score(self):
        """Test similarity search with different threshold values."""
        try:
            # Add test documents with known similarities
            texts = [
                "high_similarity",
                "medium_similarity",
                "low_similarity"
            ]
            metadatas = [
                {"id": "doc1"},
                {"id": "doc2"},
                {"id": "doc3"}
            ]
            self.vector_store.add_texts(texts=texts, metadatas=metadatas)

            results = self.vector_store.similarity_search("query", k=3, score_threshold=0.5)
            self.assertGreaterEqual(len(results), 1)
            self.assertLessEqual(len(results), 3)

        except Exception as e:
            logger.error(f"Error in test_similarity_search_with_score: {str(e)}")
            raise

    def test_empty_cache(self):
        """Test behavior when searching an empty cache."""
        try:
            results = self.vector_store.similarity_search("query", k=1, score_threshold=0.5)
            self.assertEqual(len(results), 0)
            self.assertIsInstance(results, list)
        except Exception as e:
            logger.error(f"Error in test_empty_cache: {str(e)}")
            raise

    def test_threshold_edge_cases(self):
        """Test behavior with edge case threshold values."""
        try:
            # Add multiple test documents
            texts = ["doc1", "doc2", "doc3"]
            metadatas = [{"id": f"id{i}"} for i in range(1, 4)]
            self.vector_store.add_texts(texts=texts, metadatas=metadatas)

            # Test negative threshold (means no threshold filtering)
            results = self.vector_store.similarity_search("query", k=3, score_threshold=-0.5)
            self.assertEqual(len(results), 3)  # Should get all documents up to k

            # Test threshold > 1 (no matches since similarity scores are in [0,1])
            results = self.vector_store.similarity_search("query", k=3, score_threshold=1.5)
            self.assertEqual(len(results), 0)  # Should get no results as no similarity score can exceed 1
            
            # Test with valid threshold in [0,1] range
            results = self.vector_store.similarity_search("query", k=3, score_threshold=0.5)
            self.assertLessEqual(len(results), 3)  # May get fewer results due to threshold
        except Exception as e:
            logger.error(f"Error in test_threshold_edge_cases: {str(e)}")
            raise

    def test_zero_k_value(self):
        """Test behavior with k=0."""
        try:
            self.vector_store.add_texts(
                texts=["test document"],
                metadatas=[{"id": "doc1"}]
            )
            
            with self.assertRaises(CacheError):
                self.vector_store.similarity_search("query", k=0, score_threshold=0.5)
        except Exception as e:
            logger.error(f"Error in test_zero_k_value: {str(e)}")
            raise

    def test_vector_consistency(self):
        """Test vector consistency in storage and retrieval."""
        try:
            # Add a document with known embedding
            text = "high_similarity"
            metadata = {"id": "doc1"}
            self.vector_store.add_texts([text], [metadata])

            # Query with standard Python list
            query_vector = [0.99, 0.99, 0.99, 0.99]
            # Use score_threshold=0.0 to ensure we get results
            results = self.vector_store.similarity_search_with_score_by_vector(
                query_vector,
                k=1,
                score_threshold=0.0
            )
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0][0].page_content, text)
        except Exception as e:
            logger.error(f"Error in test_vector_consistency: {str(e)}")
            raise

    def test_metadata_preservation(self):
        """Test that metadata is preserved during storage and retrieval."""
        try:
            # Add documents with metadata
            texts = ["test1"]
            metadatas = [{"id": "doc1"}]
            
            ids = self.vector_store.add_texts(
                texts=texts,
                metadatas=metadatas
            )
            self.assertEqual(len(ids), 1)

            # Search and verify metadata is preserved
            results = self.vector_store.similarity_search("test1", k=1, score_threshold=0.0)
            self.assertEqual(len(results), 1)
            
            # Verify metadata is preserved
            self.assertIn("id", results[0].metadata)
            self.assertEqual(results[0].metadata["id"], "doc1")
        except Exception as e:
            logger.error(f"Error in test_metadata_preservation: {str(e)}")
            raise

if __name__ == '__main__':
    unittest.main()