import pytest
from pygridgain import Client as Client
from langchain_gridgain.storage import GridGainStore

# Constants for testing
TEST_CACHE_NAME = "test_integration_cache"
IGNITE_HOST = "127.0.0.1"
IGNITE_PORT = 10800

@pytest.fixture(scope="module")
def ignite_client():
    client = Client()
    client.connect(IGNITE_HOST, IGNITE_PORT)
    yield client
    client.close()

@pytest.fixture(scope="function")
def gridgain_store(ignite_client):
    store = GridGainStore(TEST_CACHE_NAME, ignite_client)
    yield store
    # Clear the cache after each test
    cache = ignite_client.get_cache(TEST_CACHE_NAME)
    cache.clear()

def test_integration_mget_mset(gridgain_store):
    key_value_pairs = [("key1", "value1"), ("key2", "value2"), ("key3", "value3")]
    gridgain_store.mset(key_value_pairs)

    result = gridgain_store.mget(["key1", "key2", "key3", "non_existent_key"])
    assert result == ["value1", "value2", "value3", None]

def test_integration_mdelete(gridgain_store):
    gridgain_store.mset([("key1", "value1"), ("key2", "value2")])
    gridgain_store.mdelete(["key1", "non_existent_key"])

    result = gridgain_store.mget(["key1", "key2"])
    assert result == [None, "value2"]

def test_integration_large_dataset(gridgain_store):
    large_key_value_pairs = [("key" + str(i), "value" + str(i)) for i in range(1000)]
    gridgain_store.mset(large_key_value_pairs)

    keys = ["key" + str(i) for i in range(1000)]
    result = gridgain_store.mget(keys)
    assert len(result) == 1000
    assert all(value is not None for value in result)

def test_integration_unicode_keys(gridgain_store):
    unicode_pairs = [("🔑1", "value1"), ("키2", "value2"), ("ключ3", "value3")]
    gridgain_store.mset(unicode_pairs)

    result = gridgain_store.mget(["🔑1", "키2", "ключ3"])
    assert result == ["value1", "value2", "value3"]

def test_integration_error_handling(gridgain_store):
    with pytest.raises(Exception):
        GridGainStore("non_existent_cache", gridgain_store.client)
        raise

    disconnected_client = Client()
    with pytest.raises(Exception):
        GridGainStore(TEST_CACHE_NAME, disconnected_client)
        raise
