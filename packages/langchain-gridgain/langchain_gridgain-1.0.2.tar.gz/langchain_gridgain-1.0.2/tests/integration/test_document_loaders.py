import unittest
from pygridgain import Client
from langchain_gridgain.document_loaders import GridGainDocumentLoader
from langchain_core.documents import Document

class TestGridGainDocumentLoader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up GridGain/Apache Ignite client
        # Modify these connection details as per your GridGain/Apache Ignite setup
        cls.client = Client()
        cls.client.connect('localhost', 10800)

    @classmethod
    def tearDownClass(cls):
        cls.client.close()

    def setUp(self):
        self.cache_name = "test_document_cache"
        self.loader = GridGainDocumentLoader(
            cache_name=self.cache_name,
            client=self.client,
            create_cache_if_not_exists=True
        )
        
        # Sample data for testing
        self.sample_reviews = {
            "laptop1": "Great performance, but battery life could be better.",
            "laptop2": "Excellent build quality and keyboard. Highly recommended.",
            "laptop3": "Good value for money, but the screen could be brighter.",
        }

    def tearDown(self):
        # Clear the cache after each test
        cache = self.client.get_cache(self.cache_name)
        cache.clear()

    def test_list_caches(self):
        caches = self.loader.list_caches()
        self.assertIn(self.cache_name, caches)

    def test_populate_and_load_documents(self):
        # Populate the cache with sample data
        self.loader.populate_cache(self.sample_reviews)

        # Load documents
        documents = self.loader.load()

        # Check if all documents are loaded
        self.assertEqual(len(documents), len(self.sample_reviews))

        # Check if all loaded documents are instances of Document
        for doc in documents:
            self.assertIsInstance(doc, Document)

        # Check if all review texts are present in the loaded documents
        loaded_contents = [doc.page_content for doc in documents]
        for review in self.sample_reviews.values():
            self.assertIn(review, loaded_contents)

    def test_get_specific_document(self):
        # Populate the cache with sample data
        self.loader.populate_cache(self.sample_reviews)

        # Get a specific document
        retrieved_review = self.loader.get("laptop1")
        self.assertEqual(retrieved_review, self.sample_reviews["laptop1"])

    def test_load_with_limit(self):
        # Populate the cache with sample data
        self.loader.populate_cache(self.sample_reviews)

        # Create a new loader with a limit
        limited_loader = GridGainDocumentLoader(
            cache_name=self.cache_name,
            client=self.client,
            limit=2
        )

        # Load documents with limit
        documents = limited_loader.load()

        # Check if only 2 documents are loaded
        self.assertEqual(len(documents), 2)

    def test_load_with_filter(self):
        # Populate the cache with sample data
        self.loader.populate_cache(self.sample_reviews)

        # Create a new loader with a filter
        filtered_loader = GridGainDocumentLoader(
            cache_name=self.cache_name,
            client=self.client,
            filter_criteria={"laptop1": "Great performance, but battery life could be better."}
        )

        # Load documents with filter
        documents = filtered_loader.load()

        # Check if only the filtered document is loaded
        self.assertEqual(len(documents),3)
        self.assertEqual(documents[0].page_content, self.sample_reviews["laptop1"])

if __name__ == '__main__':
    unittest.main()