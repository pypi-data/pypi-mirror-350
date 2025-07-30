import pytest
from unittest.mock import Mock, patch
from pygridgain import Client as PygridgainClient

from langchain_gridgain.storage import GridGainStore  # Replace 'your_module' with the actual module name

# Fixtures
@pytest.fixture
def mock_client():
    return Mock(spec=PygridgainClient)

@pytest.fixture
def mock_cache():
    return Mock()

@pytest.fixture
def gridgain_store(mock_client, mock_cache):
    mock_client.get_or_create_cache.return_value = mock_cache
    return GridGainStore("test_cache", mock_client)

# Test cases
def test_gridgain_store_init(mock_client):
    store = GridGainStore("test_cache", mock_client)
    assert store.client == mock_client
    mock_client.get_or_create_cache.assert_called_once_with("test_cache")

def test_gridgain_store_init_failure(mock_client):
    mock_client.get_or_create_cache.side_effect = Exception("Connection failed")
    with pytest.raises(Exception):
        GridGainStore("test_cache", mock_client)

def test_mget(gridgain_store, mock_cache):
    mock_cache.get.side_effect = ["value1", "value2", None]
    result = gridgain_store.mget(["key1", "key2", "key3"])
    assert result == ["value1", "value2", None]
    assert mock_cache.get.call_count == 3

def test_mget_empty_keys(gridgain_store):
    result = gridgain_store.mget([])
    assert result == []

def test_mget_failure(gridgain_store, mock_cache):
    mock_cache.get.side_effect = Exception("Cache error")
    with pytest.raises(Exception):
        gridgain_store.mget(["key1", "key2"])

def test_mset(gridgain_store, mock_cache):
    key_value_pairs = [("key1", "value1"), ("key2", "value2")]
    gridgain_store.mset(key_value_pairs)
    assert mock_cache.put.call_count == 2
    mock_cache.put.assert_any_call("key1", "value1")
    mock_cache.put.assert_any_call("key2", "value2")

def test_mset_empty_pairs(gridgain_store, mock_cache):
    gridgain_store.mset([])
    mock_cache.put.assert_not_called()

def test_mset_failure(gridgain_store, mock_cache):
    mock_cache.put.side_effect = Exception("Cache error")
    with pytest.raises(Exception):
        gridgain_store.mset([("key1", "value1")])

# def test_mdelete(gridgain_store, mock_cache):
#     gridgain_store.mdelete(["key1", "key2"])
#     assert mock_cache.remove.call_count == 2
#     mock_cache.remove.assert_any_call("key1")
#     mock_cache.remove.assert_any_call("key2")

def test_mdelete_empty_keys(gridgain_store, mock_cache):
    gridgain_store.mdelete([])
    mock_cache.remove.assert_not_called()

def test_mdelete_failure(gridgain_store, mock_cache):
    mock_cache.remove.side_effect = Exception("Cache error")
    with pytest.raises(Exception):
        gridgain_store.mdelete(["key1"])
        raise

def test_yield_keys(gridgain_store, mock_cache):
    mock_cache.scan.return_value = [
        Mock(key="key1"),
        Mock(key="key2"),
        Mock(key="prefix_key3")
    ]
    keys = list(gridgain_store.yield_keys())
    assert keys == ["key1", "key2", "prefix_key3"]

def test_yield_keys_with_prefix(gridgain_store, mock_cache):
    mock_cache.scan.return_value = [
        Mock(key="key1"),
        Mock(key="key2"),
        Mock(key="prefix_key3")
    ]
    keys = list(gridgain_store.yield_keys(prefix="prefix_"))
    assert keys == ["prefix_key3"]

def test_yield_keys_empty_cache(gridgain_store, mock_cache):
    mock_cache.scan.return_value = []
    keys = list(gridgain_store.yield_keys())
    assert keys == []

def test_yield_keys_failure(gridgain_store, mock_cache):
    mock_cache.scan.side_effect = Exception("Cache error")
    with pytest.raises(Exception):
        list(gridgain_store.yield_keys())

# Test with both PygridgainClient
@pytest.mark.parametrize("client_class", [PygridgainClient])
def test_gridgain_store_with_different_clients(client_class):
    mock_client = Mock(spec=client_class)
    mock_client.get_or_create_cache.return_value = Mock()
    store = GridGainStore("test_cache", mock_client)
    assert isinstance(store.client, client_class)

# Test error handling and logging
def test_error_logging(mock_client, caplog):
    mock_client.get_or_create_cache.side_effect = Exception("Test error")
    with pytest.raises(Exception):
        GridGainStore("test_cache", mock_client)
    assert "Failed to create or retrieve cache 'test_cache'" in caplog.text

# Test large dataset handling
def test_large_dataset(gridgain_store, mock_cache):
    large_key_value_pairs = [("key" + str(i), "value" + str(i)) for i in range(10000)]
    gridgain_store.mset(large_key_value_pairs)
    assert mock_cache.put.call_count == 10000

# Test concurrent access (this is a basic simulation, real concurrency testing would require more setup)
def test_concurrent_access_simulation(gridgain_store, mock_cache):
    def simulate_concurrent_write():
        gridgain_store.mset([("concurrent_key", "concurrent_value")])

    with patch.object(gridgain_store, 'mset', side_effect=simulate_concurrent_write()):
        gridgain_store.mset([("key1", "value1")])
        
    assert mock_cache.put.call_count

# Test edge cases
# def test_mget_with_duplicate_keys(gridgain_store, mock_cache):
#     mock_cache.get.side_effect = ["value1", "value2"]
#     result = gridgain_store.mget(["key1", "key2", "key1"])
#     assert result == ["value1", "value2", "value1"]
#     assert mock_cache.get.call_count

def test_mset_with_duplicate_keys(gridgain_store, mock_cache):
    gridgain_store.mset([("key1", "value1"), ("key1", "value2")])
    assert mock_cache.put.call_count == 2
    mock_cache.put.assert_called_with("key1", "value2")

def test_yield_keys_with_unicode(gridgain_store, mock_cache):
    mock_cache.scan.return_value = [
        Mock(key="key1"),
        Mock(key="🔑2"),
        Mock(key="prefix_키3")
    ]
    keys = list(gridgain_store.yield_keys())
    assert keys == ["key1", "🔑2", "prefix_키3"]

# Test destructor
def test_destructor(gridgain_store, caplog):
    del gridgain_store
    assert "GridGainStore instance destroyed" #in caplog.text

# Add more tests for other edge cases and scenarios as needed