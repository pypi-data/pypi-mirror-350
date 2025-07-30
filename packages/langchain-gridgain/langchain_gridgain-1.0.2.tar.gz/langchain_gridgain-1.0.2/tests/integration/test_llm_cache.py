import unittest
from pygridgain import Client
import logging
from langchain_core.outputs import Generation
from langchain_gridgain.llm_cache import GridGainCache, _hash

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestGridGainCacheIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up GridGain/Apache Ignite client for all tests."""
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
        """Set up a fresh cache for each test."""
        self.cache_name = "test_llm_cache"
        try:
            self.cache = GridGainCache(
                cache_name=self.cache_name,
                client=self.client
            )
            logger.info(f"Created test cache: {self.cache_name}")
        except Exception as e:
            logger.error(f"Failed to create test cache: {e}")
            raise

    def tearDown(self):
        """Clean up after each test."""
        try:
            self.cache.clear()
            logger.info(f"Cleared test cache: {self.cache_name}")
        except Exception as e:
            logger.error(f"Error clearing test cache: {e}")

    def test_cache_lookup_update(self):
        """Test basic cache update and lookup functionality."""
        test_prompt = "What is the capital of France?"
        test_llm = "test_llm"
        test_generations = [Generation(text="The capital of France is Paris.")]

        # Update cache
        self.cache.update(test_prompt, test_llm, test_generations)
        logger.info("Successfully updated cache")

        # Lookup and verify
        result = self.cache.lookup(test_prompt, test_llm)
        self.assertIsNotNone(result, "Cache lookup returned None")
        self.assertEqual(len(result), 1, "Expected exactly one generation")
        self.assertEqual(result[0].text, test_generations[0].text,
                        "Retrieved text doesn't match stored text")

    def test_case_insensitive_lookup(self):
        """Test that cache lookups are case-insensitive."""
        lower_prompt = "what is python?"
        upper_prompt = "WHAT IS PYTHON?"
        test_llm = "test_llm"
        test_generations = [Generation(text="Python is a programming language.")]

        # Store with lowercase
        self.cache.update(lower_prompt, test_llm, test_generations)

        # Lookup with uppercase
        result = self.cache.lookup(upper_prompt, test_llm)
        self.assertIsNotNone(result)
        self.assertEqual(result[0].text, test_generations[0].text)

    def test_multiple_generations(self):
        """Test storing and retrieving multiple generations."""
        test_prompt = "Generate three greetings"
        test_llm = "test_llm"
        test_generations = [
            Generation(text="Hello!"),
            Generation(text="Hi there!"),
            Generation(text="Good morning!")
        ]

        self.cache.update(test_prompt, test_llm, test_generations)

        result = self.cache.lookup(test_prompt, test_llm)
        self.assertEqual(len(result), 3)
        for orig, retrieved in zip(test_generations, result):
            self.assertEqual(orig.text, retrieved.text)

    def test_cache_update_existing(self):
        """Test updating an existing cache entry."""
        test_prompt = "test prompt"
        test_llm = "test_llm"
        original_generations = [Generation(text="original response")]
        updated_generations = [Generation(text="updated response")]

        # First update
        self.cache.update(test_prompt, test_llm, original_generations)
        
        # Second update
        self.cache.update(test_prompt, test_llm, updated_generations)

        # Verify the update
        result = self.cache.lookup(test_prompt, test_llm)
        self.assertEqual(result[0].text, "updated response")

    def test_delete_entry(self):
        """Test deleting a cache entry."""
        test_prompt = "test prompt for deletion"
        test_llm = "test_llm"
        test_generations = [Generation(text="test response")]
        
        # Add and verify entry
        self.cache.update(test_prompt, test_llm, test_generations)
        self.assertIsNotNone(self.cache.lookup(test_prompt, test_llm))
        
        # Delete and verify deletion
        self.cache.delete(test_prompt, test_llm)
        self.assertIsNone(self.cache.lookup(test_prompt, test_llm))

    def test_large_text_handling(self):
        """Test handling of large text content."""
        large_text = "Large text content " * 1000  # Create a large string
        test_generations = [Generation(text=large_text)]
        
        self.cache.update("large_prompt", "test_llm", test_generations)
        result = self.cache.lookup("large_prompt", "test_llm")
        
        self.assertIsNotNone(result)
        self.assertEqual(result[0].text, large_text)

    def test_special_characters(self):
        """Test handling of special characters in prompts."""
        special_prompt = "!@#$%^&*()_+ Special चरित्र"
        test_generations = [Generation(text="Special response")]
        
        self.cache.update(special_prompt, "test_llm", test_generations)
        result = self.cache.lookup(special_prompt, "test_llm")
        
        self.assertIsNotNone(result)
        self.assertEqual(result[0].text, test_generations[0].text)

if __name__ == '__main__':
    unittest.main()