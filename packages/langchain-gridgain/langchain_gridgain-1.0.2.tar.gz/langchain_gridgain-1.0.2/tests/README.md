# GridGain LangChain Tests

This repository contains a comprehensive test suite for the GridGain integration with LangChain. The test suite includes both unit tests and integration tests covering various components of the integration, such as document loading, LLM caching, vector storage, chat message history, and general storage operations.

## Test Files

### Unit Tests
1. `test_chat_message_histories.py`
2. `test_document_loaders.py`
3. `test_llm_cache.py`
4. `test_storage.py`
5. `test_vectorstores.py`

### Integration Tests
1. `test_chat_message_histories.py`
2. `test_document_loaders.py`
3. `test_llm_cache.py`
4. `test_storage.py`
5. `test_vectorstores.py`

## Prerequisites

- Python 3.11.7+
- pytest
- unittest
- pyignite
- Running GridGain/Apache Ignite (for integration tests)

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/gridgain-poc/gg8_langchain.git
   cd gg8_langchain
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the package and its dependencies:
   ```
   pip install -e '.[test,coverage]'
   ```
4. For integration tests, ensure GridGain is set up and running with vector serach enabled. Adjust the connection details (host and port) in the test files to match your GridGain configuration.

## Running the Tests

To run all tests, execute the following command in the root directory of the project:

```
pytest
```

To run a specific test file, use:

```
pytest tests/unit/test_chat_message_histories.py
pytest tests/integration/test_chat_message_histories_history.py
```

To run all tests in a specific directory:

```
pytest tests/unit
pytest tests/integration
```

## Test Descriptions

### Unit Tests

#### 1. test_chat_message_histories.py
Unit tests for GridGainChatMessageHistory class:
- Cache initialization and custom naming
- Message serialization/deserialization
- Session isolation
- Error handling and cleanup

#### 2. test_document_loaders.py
Unit tests for GridGainDocumentLoader class:
- Cache operations and listings
- Document loading with filters
- Pagination and limits
- Metadata handling
- Client type compatibility

#### 3. test_llm_cache.py
Unit tests for GridGainCache class:
- Cache initialization and configuration
- Generation lookup/storage
- Case sensitivity handling
- Error states and malformed data
- LLM-specific operations

#### 4. test_storage.py
Unit tests for GridGainStore class:
- Batch operations (mget, mset, mdelete)
- Key iteration and filtering
- Large dataset handling
- Concurrency simulations
- Unicode support
- Error handling

#### 5. test_vectorstores.py
Unit tests for GridGainVectorStore class:
- Document addition with embeddings
- Similarity search with scores
- Metadata preservation
- Threshold behavior
- Vector consistency
- Multiple search patterns

### Integration Tests

#### 1. test_chat_message_histories.py
Integration tests for the GridGainChatMessageHistory class.

Key tests include:
- Adding and retrieving long message sequences
- Message clearing functionality
- Session isolation with multiple sessions

#### 2. test_document_loaders.py
Integration tests for the GridGainDocumentLoader class.

Key tests include:
- Cache listing verification
- Document population and loading
- Specific document retrieval
- Limit-based document loading
- Filter-based document loading

#### 3. test_llm_cache.py
Integration tests for the GridGainCache class.

Key tests include:
- Cache lookup/update functionality
- Case-insensitive lookup
- Multiple generation handling
- Cache entry updates
- Entry deletion
- Large text handling
- Special character support

#### 4. test_semantic_llm_cache.py
Integration tests for the GridGainSemanticCache class.

Key tests include:
- Semantic similarity based lookups
- Threshold-based filtering
- Cache update functionality
- Multiple similar query handling

#### 5. test_storage.py
Integration tests for the GridGainStore class.

Key tests include:
- Multi-get/set operations
- Multi-delete operations
- Large dataset handling
- Unicode key support
- Error handling

#### 6. test_vectorstores.py
Integration tests for the GridGainVectorStore class.

Key tests include:
- Similarity search with scores
- Empty cache behavior
- Threshold edge cases
- Zero k-value handling
- Vector consistency
- Metadata preservation