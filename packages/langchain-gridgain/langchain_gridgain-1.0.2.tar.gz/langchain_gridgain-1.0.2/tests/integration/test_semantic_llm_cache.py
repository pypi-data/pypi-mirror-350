import unittest
from pygridgain import Client
import logging
from langchain_core.outputs import Generation
from langchain_core.embeddings import Embeddings
from langchain_gridgain.llm_cache import GridGainSemanticCache, GridGainCache

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MockEmbeddings(Embeddings):
    """Mock embeddings that simulate semantic similarity."""
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        base_vectors = {
            "capital france": [1.0, 0.0, 0.0, 0.0],  # vector for capital
            "population": [0.0, 1.0, 0.0, 0.0], # completely different vector for population
        }
        
        embeddings = []
        for text in texts:
            text = text.lower()
            if any(phrase in text for phrase in [
                "capital of france",
                "france's capital",
                "french capital",
                "capital city of france"
            ]):
                embeddings.append(base_vectors["capital france"])
            elif "population" in text:
                embeddings.append(base_vectors["population"])
            else:
                embeddings.append([0.1, 0.1, 0.1, 0.1])  # Default vector
        return embeddings

    def embed_query(self, text: str) -> list[float]:
        return self.embed_documents([text])[0]

class TestGridGainSemanticCacheIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up GridGain client for all tests."""
        try:
            cls.client = Client()
            cls.client.connect('localhost', 10800)
            logger.info("Successfully connected to GridGain server")
        except Exception as e:
            logger.error(f"Failed to connect to GridGain server: {e}")
            raise

    @classmethod
    def tearDownClass(cls):
        """Close the client connection."""
        try:
            cls.client.close()
            logger.info("Successfully closed GridGain connection")
        except Exception as e:
            logger.error(f"Error closing GridGain connection: {e}")

    def setUp(self):
        """Set up fresh caches for each test."""
        try:
            self.llm_cache = GridGainCache("test_llm_cache", self.client)
            self.embeddings = MockEmbeddings()
            self.cache = GridGainSemanticCache(
                llm_cache=self.llm_cache,
                cache_name="test_semantic_cache",
                client=self.client,
                embedding=self.embeddings,
                similarity_threshold=0.9
            )
            self.llm_cache.clear()
            self.cache.vector_store.cache.clear()
            logger.info("Created and cleared test caches")
        except Exception as e:
            logger.error(f"Failed to create test caches: {e}")
            raise

    def tearDown(self):
        """Clean up after each test."""
        try:
            self.llm_cache.clear()
            self.cache.vector_store.cache.clear()
            logger.info("Cleared test caches")
        except Exception as e:
            logger.error(f"Error clearing test caches: {e}")

    def test_cache_lookup_update(self):
        """Test basic semantic cache functionality with similar queries."""
        original_prompt = "What's the capital of France?"
        similar_prompt = "Tell me France's capital city"
        test_generations = [Generation(text="Paris is the capital")]
        
        # Update cache with the first prompt
        self.cache.update(original_prompt, "test_llm", test_generations)
        
        # Look up with second prompt which is similar to the first
        result = self.cache.lookup(similar_prompt, "test_llm")
        self.assertIsNotNone(result, "Should find result for similar prompt")
        self.assertEqual(result[0].text, test_generations[0].text)

    def test_similarity_threshold(self):
        """Test semantic similarity threshold filtering."""
        original_prompt = "What's the capital of France?"
        dissimilar_prompt = "What's the population of Paris?"
        generations = [Generation(text="Paris is the capital")]
        
        self.cache.update(original_prompt, "test_llm", generations)
        
        # Test with the population prompt (should miss)
        dissimilar_result = self.cache.lookup(dissimilar_prompt, "test_llm")
        self.assertIsNone(dissimilar_result, "Should not find result for dissimilar prompt")

    def test_cache_update_existing(self):
        """Test updating existing semantic cache entry."""
        prompt = "What's the capital of France?"
        original_gen = [Generation(text="Original: Paris")]
        updated_gen = [Generation(text="Updated: Paris, the capital of France")]
        
        # First update
        self.cache.update(prompt, "test_llm", original_gen)
        first_result = self.cache.lookup(prompt, "test_llm")
        self.assertEqual(first_result[0].text, original_gen[0].text)
        
        # Second update
        self.cache.update(prompt, "test_llm", updated_gen)
        second_result = self.cache.lookup(prompt, "test_llm")
        self.assertEqual(second_result[0].text, updated_gen[0].text)

    def test_multiple_similar_queries(self):
        """Test multiple semantically similar queries."""
        base_prompt = "What is the capital of France?"
        variations = [
            "Tell me France's capital city",
            "What's the French capital?",
            "Which city is France's capital?"
        ]
        generations = [Generation(text="Paris is the capital")]
        
        self.cache.update(base_prompt, "test_llm", generations)
        for variant in variations:
            result = self.cache.lookup(variant, "test_llm")
            self.assertIsNotNone(result, f"Should find result for similar prompt: {variant}")
            self.assertEqual(result[0].text, generations[0].text)

if __name__ == '__main__':
    unittest.main()