import pytest
from unittest.mock import Mock, patch
from langchain_core.embeddings import Embeddings
from langchain_core.documents import Document
from pygridgain.datatypes import FloatArrayObject
from langchain_gridgain.vectorstores import GridGainVectorStore, Article

class MockEmbeddings(Embeddings):
    def embed_documents(self, texts):
        return [[0.1, 0.2, 0.3] for _ in texts]

    def embed_query(self, text):
        return [0.1, 0.2, 0.3]

@pytest.fixture
def mock_client():
    return Mock()

@pytest.fixture
def mock_cache():
    return Mock()

@pytest.fixture
def vector_store(mock_client):
    embedding = MockEmbeddings()
    return GridGainVectorStore(
        cache_name="test_cache",
        embedding=embedding,
        client=mock_client
    )

def test_init(vector_store):
    assert vector_store.cache_name == "test_cache"
    assert isinstance(vector_store.embedding, Embeddings)

def test_embeddings_property(vector_store):
    assert isinstance(vector_store.embeddings, Embeddings)

def test_add_texts(vector_store, mock_client, mock_cache):
    mock_client.get_cache.return_value = mock_cache
    texts = ["Test document 1", "Test document 2"]
    metadatas = [{"id": "1"}, {"id": "2"}]
    
    # Create expected Article objects
    expected_embedding = [0.1, 0.2, 0.3]
    expected_articles = [
        Article(content=text, contentVector=expected_embedding)
        for text in texts
    ]
    
    titles = vector_store.add_texts(texts, metadatas=metadatas)
    
    # Verify cache interactions
    assert mock_client.get_cache.called_with("test_cache")
    assert len(titles) == 2
    assert titles == ["1", "2"]
    
    # Verify correct Article objects were stored
    calls = mock_cache.put.call_args_list
    assert len(calls) == 2
    for i, call in enumerate(calls):
        args = call[0]
        assert args[0] == str(i + 1)  # id
        assert isinstance(args[1], Article)
        assert args[1].content == texts[i]
        assert args[1].contentVector == expected_embedding

def test_similarity_search_with_score_by_vector(vector_store, mock_client, mock_cache):
    mock_client.get_cache.return_value = mock_cache
    
    # Mock the vector search cursor with proper 3-tuple return values
    mock_cursor = Mock()
    mock_cursor.__iter__ = Mock(return_value=iter([
        ("1", Article(content="Test content 1", contentVector=[0.1, 0.2, 0.3])),
        ("2", Article(content="Test content 2", contentVector=[0.2, 0.3, 0.4]))
    ]))
    mock_cache.vector.return_value = mock_cursor
    
    results = vector_store.similarity_search_with_score_by_vector([0.1, 0.2, 0.3], k=2, score_threshold=0.6)
    
    # Verify cache interactions
    mock_client.get_cache.assert_called_with("test_cache")
    mock_cache.vector.assert_called_once()
    
    # Verify results
    assert len(results) == 2
    for doc, score in results:
        assert isinstance(doc, Document)
        assert isinstance(score, float)
        assert doc.page_content in ["Test content 1", "Test content 2"]
        assert "id" in doc.metadata

def test_similarity_search(vector_store, mock_client, mock_cache):
    mock_client.get_cache.return_value = mock_cache
    
    # Mock the vector search cursor with score
    mock_cursor = Mock()
    mock_cursor.__iter__ = Mock(return_value=iter([
        ("1", Article(content="Test content 1", contentVector=[0.1, 0.2, 0.3]))
    ]))
    mock_cache.vector.return_value = mock_cursor
    
    results = vector_store.similarity_search("test query", k=1)
    
    # Verify results
    assert len(results) == 1
    assert isinstance(results[0], Document)
    assert results[0].page_content == "Test content 1"
    assert results[0].metadata["id"] == "1"

if __name__ == '__main__':
    pytest.main()