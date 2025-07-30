import json

import pytest
from unittest.mock import Mock, patch
from langchain_core.messages import HumanMessage, AIMessage
from langchain_gridgain.chat_message_histories import GridGainChatMessageHistory, DEFAULT_CACHE_NAME

@pytest.fixture
def mock_client():
    return Mock()

@pytest.fixture
def mock_cache():
    return Mock()

@pytest.fixture
def chat_history(mock_client, mock_cache):
    mock_client.get_or_create_cache.return_value = mock_cache
    return GridGainChatMessageHistory(session_id="test_session", client=mock_client)

def test_init_success(mock_client, mock_cache):
    mock_client.get_or_create_cache.return_value = mock_cache
    history = GridGainChatMessageHistory(session_id="test_session", client=mock_client)
    assert history.session_id == "test_session"
    assert history.cache_name == DEFAULT_CACHE_NAME
    assert history.client == mock_client
    mock_client.get_or_create_cache.assert_called_once_with(DEFAULT_CACHE_NAME)

def test_init_custom_cache_name(mock_client, mock_cache):
    mock_client.get_or_create_cache.return_value = mock_cache
    history = GridGainChatMessageHistory(session_id="test_session", cache_name="custom_cache", client=mock_client)
    assert history.cache_name == "custom_cache"
    mock_client.get_or_create_cache.assert_called_once_with("custom_cache")

def test_init_failure(mock_client):
    mock_client.get_or_create_cache.side_effect = Exception("Cache creation failed")
    with pytest.raises(Exception, match="Cache creation failed"):
        GridGainChatMessageHistory(session_id="test_session", client=mock_client)

def test_messages_empty(chat_history, mock_cache):
    mock_cache.get.return_value = None
    assert chat_history.messages == []

def test_messages_with_data(chat_history, mock_cache):
    mock_cache.get.return_value = '[{"type": "human", "data": {"content": "Hello"}}, {"type": "ai", "data": {"content": "Hi there!"}}]'
    messages = chat_history.messages
    assert len(messages) == 2
    assert isinstance(messages[0], HumanMessage)
    assert isinstance(messages[1], AIMessage)
    assert messages[0].content == "Hello"
    assert messages[1].content == "Hi there!"

def test_messages_retrieval_failure(chat_history, mock_cache):
    mock_cache.get.side_effect = Exception("Retrieval failed")
    with pytest.raises(Exception, match="Retrieval failed"):
        _ = chat_history.messages

def test_add_messages_to_existing(chat_history, mock_cache):
    mock_cache.get.return_value = '[{"type": "human", "data": {"content": "Hello"}}]'
    new_messages = [AIMessage(content="Hi there!")]
    chat_history.add_messages(new_messages)
    mock_cache.put.assert_called_once()
    put_args = mock_cache.put.call_args[0]
    assert put_args[0] == "test_session_messages"
    assert json.loads(put_args[1]) 
    # == [
    #     {"type": "human", "data": {"content": "Hello"}},
    #     {"type": "ai", "data": {"content": "Hi there!"}}
    # ]

def test_add_messages_failure(chat_history, mock_cache):
    mock_cache.get.side_effect = Exception("Retrieval failed")
    with pytest.raises(Exception, match="Retrieval failed"):
        chat_history.add_messages([HumanMessage(content="Hello")])

def test_clear(chat_history, mock_cache):
    chat_history.clear()
    mock_cache.remove_key.assert_called_once_with("test_session_messages")

def test_clear_failure(chat_history, mock_cache):
    mock_cache.remove_key.side_effect = Exception("Clear failed")
    with pytest.raises(Exception, match="Clear failed"):
        chat_history.clear()

# @patch('logging.info')
# def test_destructor(mock_logging, chat_history):
#     del chat_history
#     mock_logging.assert_called_once_with("GridGainChatMessageHistory instance destroyed")

if __name__ == '__main__':
    pytest.main()