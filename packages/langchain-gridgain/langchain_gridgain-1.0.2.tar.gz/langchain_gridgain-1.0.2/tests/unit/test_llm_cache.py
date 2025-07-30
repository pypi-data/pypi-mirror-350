import unittest
from unittest.mock import Mock, patch
import json
from langchain_core.outputs import Generation
from langchain_core.language_models import LLM
from langchain_gridgain.llm_cache import GridGainCache, _hash

class TestGridGainCache(unittest.TestCase):
    def setUp(self):
        self.mock_client = Mock()
        self.mock_cache = Mock()
        self.mock_client.get_or_create_cache.return_value = self.mock_cache
        self.cache_name = "test_llm_cache"
        self.cache = GridGainCache(self.cache_name, self.mock_client)
        self.test_generation = Generation(text="Test generation")

    def test_init_success(self):
        self.assertEqual(self.cache.cache_name, self.cache_name)
        self.assertEqual(self.cache.client, self.mock_client)
        self.mock_client.get_or_create_cache.assert_called_once_with(self.cache_name)

    def test_init_failure(self):
        self.mock_client.get_or_create_cache.side_effect = Exception("Cache creation failed")
        with self.assertRaises(Exception):
            GridGainCache(self.cache_name, self.mock_client)

    def test_make_id(self):
        prompt = "test prompt"
        llm_string = "test llm"
        expected_id = _hash(prompt.strip().lower())
        self.assertEqual(GridGainCache._make_id(prompt, llm_string), expected_id)

    def test_lookup_success(self):
        test_prompt = "test prompt"
        test_llm = "test llm"
        expected_generations = [self.test_generation]
        cached_data = json.dumps([gen.dict() for gen in expected_generations])
        
        self.mock_cache.get.return_value = cached_data
        
        result = self.cache.lookup(test_prompt, test_llm)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, self.test_generation.text)
        self.mock_cache.get.assert_called_once_with(_hash(test_prompt.strip().lower()))

    def test_lookup_with_mixed_case_prompt(self):
        mixed_case_prompt = "Test PROMPT  "
        cached_generations = [self.test_generation]
        self.mock_cache.get.return_value = json.dumps([gen.dict() for gen in cached_generations])
        
        result = self.cache.lookup(mixed_case_prompt, "test_llm")
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, self.test_generation.text)
        self.mock_cache.get.assert_called_once_with(_hash(mixed_case_prompt.strip().lower()))

    def test_lookup_cache_miss(self):
        self.mock_cache.get.return_value = None
        result = self.cache.lookup("test prompt", "test llm")
        self.assertIsNone(result)

    def test_lookup_malformed_data(self):
        self.mock_cache.get.return_value = "invalid json"
        result = self.cache.lookup("test prompt", "test llm")
        self.assertIsNone(result)

    def test_update(self):
        test_prompt = "test prompt"
        test_llm = "test llm"
        generations = [self.test_generation]
        
        self.cache.update(test_prompt, test_llm, generations)
        
        self.mock_cache.put.assert_called_once()
        call_args = self.mock_cache.put.call_args[0]
        self.assertEqual(call_args[0], _hash(test_prompt.strip().lower()))
        self.assertIsInstance(call_args[1], str)

    def test_update_with_error(self):
        self.mock_cache.put.side_effect = Exception("Update failed")
        with self.assertRaises(Exception):
            self.cache.update("test prompt", "test llm", [self.test_generation])

    def test_delete(self):
        test_prompt = "test prompt"
        test_llm = "test llm"
        
        self.cache.delete(test_prompt, test_llm)
        self.mock_cache.remove_key.assert_called_once_with(_hash(test_prompt.strip().lower()))

    def test_delete_with_error(self):
        self.mock_cache.remove_key.side_effect = Exception("Delete failed")
        with self.assertRaises(Exception):
            self.cache.delete("test prompt", "test llm")

    def test_clear(self):
        self.cache.clear()
        self.mock_cache.clear.assert_called_once()

    def test_clear_with_error(self):
        self.mock_cache.clear.side_effect = Exception("Clear failed")
        with self.assertRaises(Exception):
            self.cache.clear()

    def test_delete_through_llm(self):
        test_prompt = "test prompt"
        mock_llm = Mock(spec=LLM)
        mock_llm.dict.return_value = {}
        
        # Use the correct import path - langchain_gridgain instead of langchain_community
        with patch('langchain_gridgain.llm_cache.get_prompts', 
                return_value=('', 'test llm string')):
            self.cache.delete_through_llm(test_prompt, mock_llm)
            self.cache.cache.remove_key.assert_called_once_with(
                _hash(test_prompt.strip().lower())
            )

if __name__ == '__main__':
    unittest.main()