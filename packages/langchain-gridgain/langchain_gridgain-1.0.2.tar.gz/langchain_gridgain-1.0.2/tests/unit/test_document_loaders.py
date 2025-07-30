import pytest
from unittest.mock import Mock, patch
from pygridgain import Client as PygridgainClient
from langchain_core.documents import Document

from langchain_gridgain.document_loaders import GridGainDocumentLoader  # Replace 'your_module' with the actual module name

@pytest.fixture
def mock_client():
    return Mock(spec=PygridgainClient)

@pytest.fixture
def mock_cache():
    return Mock()

@pytest.fixture
def sample_data():
    return {
        "key1": "value1",
        "key2": "value2",
        "key3": "value3",
    }

def test_init_success(mock_client):
    loader = GridGainDocumentLoader("test_cache", mock_client)
    assert loader.cache_name == "test_cache"
    assert loader.client == mock_client
    mock_client.get_or_create_cache.assert_called_once_with("test_cache")

def test_init_failure(mock_client):
    mock_client.get_or_create_cache.side_effect = Exception("Connection failed")
    with pytest.raises(Exception):
        GridGainDocumentLoader("test_cache", mock_client)

def test_list_caches(mock_client):
    mock_client.get_cache_names.return_value = ["cache1", "cache2"]
    loader = GridGainDocumentLoader("test_cache", mock_client)
    assert loader.list_caches() == ["cache1", "cache2"]

def test_list_caches_failure(mock_client):
    mock_client.get_cache_names.side_effect = Exception("Connection failed")
    loader = GridGainDocumentLoader("test_cache", mock_client)
    with pytest.raises(Exception):
        loader.list_caches()

def test_populate_cache(mock_client, mock_cache, sample_data):
    mock_client.get_or_create_cache.return_value = mock_cache
    loader = GridGainDocumentLoader("test_cache", mock_client)
    loader.populate_cache(sample_data)
    for key, value in sample_data.items():
        mock_cache.put.assert_any_call(key, value)

# def test_populate_cache_failure(mock_client):
#     mock_client.get_or_create_cache.side_effect = Exception("Cache creation failed")
#     loader = GridGainDocumentLoader("test_cache", mock_client)
#     with pytest.raises(Exception):
#         loader.populate_cache({"key": "value"})

def test_get(mock_client, mock_cache):
    mock_client.get_or_create_cache.return_value = mock_cache
    mock_cache.get.return_value = "test_value"
    loader = GridGainDocumentLoader("test_cache", mock_client)
    assert loader.get("test_key") == "test_value"

# def test_get_failure(mock_client):
#     mock_client.get_or_create_cache.side_effect = Exception("Cache retrieval failed")
#     loader = GridGainDocumentLoader("test_cache", mock_client)
#     with pytest.raises(Exception):
#         loader.get("test_key")

def test_load_success(mock_client, mock_cache, sample_data):
    mock_client.get_cache.return_value = mock_cache
    mock_cache.scan.return_value = sample_data.items()
    loader = GridGainDocumentLoader("test_cache", mock_client)
    documents = loader.load()
    assert len(documents) == len(sample_data)
    for doc in documents:
        assert isinstance(doc, Document)
        assert doc.page_content in sample_data.values()
        assert doc.metadata["cache"] == "test_cache"

def test_load_with_limit(mock_client, mock_cache, sample_data):
    mock_client.get_cache.return_value = mock_cache
    mock_cache.scan.return_value = sample_data.items()
    loader = GridGainDocumentLoader("test_cache", mock_client, limit=2)
    documents = loader.load()
    assert len(documents) == 2

def test_load_empty_cache(mock_client, mock_cache):
    mock_client.get_cache.return_value = mock_cache
    mock_cache.scan.return_value = []
    loader = GridGainDocumentLoader("test_cache", mock_client)
    documents = loader.load()
    assert len(documents) == 0

def test_load_failure(mock_client):
    mock_client.get_cache.side_effect = Exception("Cache retrieval failed")
    loader = GridGainDocumentLoader("test_cache", mock_client)
    with pytest.raises(Exception):
        loader.load()

@pytest.mark.parametrize("client_class", [PygridgainClient])
def test_client_types(client_class):
    mock_client = Mock(spec=client_class)
    loader = GridGainDocumentLoader("test_cache", mock_client)
    assert isinstance(loader.client, client_class)

def test_filter_criteria():
    mock_client = Mock(spec=PygridgainClient)
    mock_cache = Mock()
    mock_client.get_cache.return_value = mock_cache
    sample_data = {
        "key1": {"field1": "value1", "field2": "value2"},
        "key2": {"field1": "value3", "field2": "value4"},
    }
    mock_cache.scan.return_value = sample_data.items()
    
    loader = GridGainDocumentLoader("test_cache", mock_client, filter_criteria={"field1": "value1"})
    documents = loader.load()
    assert len(documents)
    assert documents[0].page_content == str({"field1": "value1", "field2": "value2"})

# def test_create_cache_if_not_exists():
#     mock_client = Mock(spec=Client)
#     GridGainDocumentLoader("test_cache", mock_client, create_cache_if_not_exists=True)
#     mock_client.get_or_create_cache.assert_called_once_with("test_cache")

#     mock_client.reset_mock()
#     GridGainDocumentLoader("test_cache", mock_client, create_cache_if_not_exists=False)
#     mock_client.get_or_create_cache.assert_not_called()

# Add more tests for _matches_filter method and other corner cases as needed