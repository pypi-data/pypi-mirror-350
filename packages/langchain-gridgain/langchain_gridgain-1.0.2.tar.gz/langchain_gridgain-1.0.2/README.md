# langchain-gridgain

langchain-gridgain is a Python library that provides seamless integration between GridGain/Apache Ignite and LangChain. This library offers a set of storage adapters that allow LangChain components to efficiently use GridGain as a backend for various data storage needs.

## Table of Contents
1. [Features](#features)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [GridGain Setup](#gridgain-setup)
   - [Connecting to GridGain](#1-connecting-to-gridgain)
5. [Detailed Component Explanations](#detailed-component-explanations)
   - [GridGainStore](#1-gridgainstore)
   - [GridGainDocumentLoader](#2-gridgaindocumentloader)
   - [GridGainChatMessageHistory](#3-gridgainchatmessagehistory)
   - [GridGainCache](#4-gridgaincache)
   - [GridGainSemanticCache](#5-gridgainsemanticcache)
   - [GridGainVectorStore](#6-gridgainvectorstore)
5. [Documentation](#documentation)
6. [Example](#example)

## Features

This library implements five key LangChain interfaces for GridGain:

1. **GridGainStore**: A key-value store implementation.
2. **GridGainDocumentLoader**: A document loader for retrieving documents from GridGain caches.
3. **GridGainChatMessageHistory**: A chat message history store using GridGain.
4. **GridGainCache**: A caching mechanism for Language Models using GridGain.
5. **GridGainSemanticCache**: A semantic caching mechanism for Language Models using GridGain.
6. **GridGainVectorStore**: A vector store implementation using GridGain for storing and querying embeddings.


## Prerequisites

1. Python 3.10 or above (3.11, 3.12 and 3.13 are tested)
    * You can use `pyenv` to manage multiple Python versions (optional):
        1. Install `pyenv`: `brew install pyenv` (or your system's package manager)
        2. Create and activate the environment: 
            ```bash
            pyenv virtualenv 3.11.7 langchain-env
            source $HOME/.pyenv/versions/langchain-env/bin/activate 
            ```
    * Alternatively, ensure supported Python version is installed directly.

2. A running GridGain Enterprise or Ultimate Edition, at least 8.9.17 ([release notes](https://www.gridgain.com/docs/latest/release-notes/8.9.17/release-notes_8.9.17))
   - Make sure your license includes access to the vector search feature.

## Installation

Install the package using pip:

```bash
pip install langchain-gridgain
```

## GridGain Setup

In order to use [GridGain](https://www.gridgain.com/) powered langchain components, you need to have a running GridGain cluster with vector search enabled.

### 1. Connecting to Gridgain

```python
from pygridgain import Client

def connect_to_gridgain(host: str, port: int) -> Client:
    try:
        client = Client()
        client.connect(host, port)
        print("Connected to Ignite successfully.")
        return client
    except Exception as e:
        print(f"Failed to connect to Ignite: {e}")
        raise
```

Usage:
```python
client = connect_to_gridgain("localhost", 10800)
```

## Detailed Component Explanations

### 1. GridGainStore

GridGainStore is a key-value store implementation that uses GridGain as its backend. It provides a simple and efficient way to store and retrieve data using key-value pairs.

Usage example:
```python
from langchain_gridgain.storage import GridGainStore

def initialize_keyvalue_store(client) -> GridGainStore:
    try:
        key_value_store = GridGainStore(
            cache_name="laptop_specs",
            client=client
        )
        print("GridGainStore initialized successfully.")
        return key_value_store
    except Exception as e:
        print(f"Failed to initialize GridGainStore: {e}")
        raise

# Usage
client = connect_to_ignite("localhost", 10800)
key_value_store = initialize_keyvalue_store(client)

# Store a value
key_value_store.mset([("laptop1", "16GB RAM, NVIDIA RTX 3060, Intel i7 11th Gen")])

# Retrieve a value
specs = key_value_store.mget(["laptop1"])[0]
```

### 2. GridGainDocumentLoader

GridGainDocumentLoader is designed to load documents from GridGain caches. It's particularly useful for scenarios where you need to retrieve and process large amounts of textual data stored in GridGain.

Usage example:
```python
from langchain_gridgain.document_loaders import GridGainDocumentLoader

def initialize_doc_loader(client) -> GridGainDocumentLoader:
    try:
        doc_loader = GridGainDocumentLoader(
            cache_name="review_cache",
            client=client,
            create_cache_if_not_exists=True
        )
        print("GridGainDocumentLoader initialized successfully.")
        return doc_loader
    except Exception as e:
        print(f"Failed to initialize GridGainDocumentLoader: {e}")
        raise

# Usage
client = connect_to_ignite("localhost", 10800)
doc_loader = initialize_doc_loader(client)

# Populate the cache
reviews = {
    "laptop1": "Great performance for coding and video editing. The 16GB RAM and dedicated GPU make multitasking a breeze."
}
doc_loader.populate_cache(reviews)

# Load documents
documents = doc_loader.load()
```

### 3. GridGainChatMessageHistory

GridGainChatMessageHistory provides a way to store and retrieve chat message history using GridGain. This is crucial for maintaining context in conversational AI applications.

Usage example:
```python
from langchain_gridgain.chat_message_histories import GridGainChatMessageHistory

def initialize_chathistory_store(client) -> GridGainChatMessageHistory:
    try:
        chat_history = GridGainChatMessageHistory(
            session_id="user_session",
            cache_name="chat_history",
            client=client
        )
        print("GridGainChatMessageHistory initialized successfully.")
        return chat_history
    except Exception as e:
        print(f"Failed to initialize GridGainChatMessageHistory: {e}")
        raise

# Usage
client = connect_to_ignite("localhost", 10800)
chat_history = initialize_chathistory_store(client)

# Add a message to the history
chat_history.add_user_message("Hello, I need help choosing a laptop.")

# Retrieve the conversation history
messages = chat_history.messages
```

### 4. GridGainCache

GridGainCache provides a caching mechanism for the responses received from LLMs using GridGain. This can significantly improve response times for **exact** queries by storing and retrieving pre-computed results.

Usage example:

```python
from langchain_gridgain.llm_cache import GridGainCache

def initialize_llm_cache(client)-> GridGainCache:
    try:
        llm_cache = GridGainCache(
            cache_name="llm_cache",
            client=client
        )
        logger.info("GridGainCache initialized successfully.")
        return llm_cache
    except Exception as e:
        logger.error(f"Failed to initialize GridGainCache: {e}")
        raise
```

### 5. GridGainSemanticCache

GridGainSemanticCache provides a semantic caching mechanism for the responses received from LLMs using GridGain. This can significantly improve response times for **similar** queries by storing and retrieving pre-computed results.

Usage example:

```python
from langchain_gridgain.llm_cache import GridGainCache
from langchain_gridgain.llm_cache import GridGainSemanticCache


def initialize_semantic_llm_cache(client, embedding)-> GridGainSemanticCache:
    try:
        llm_cache = GridGainCache(
            cache_name="llm_cache",
            client=client
        )
        semantic_cache = GridGainSemanticCache(
            llm_cache=llm_cache,
            cache_name="semantic_llm_cache",
            client=client,
            embedding=embedding,
            similarity_threshold=0.85
        )
        logger.info("GridGainSemanticCache initialized successfully.")
        return semantic_cache
    except Exception as e:
        logger.error(f"Failed to initialize GridGainSemanticCache: {e}")
        raise

### 6. GridGainVectorStore

GridGainVectorStore is a vector store implementation using GridGain for storing and querying embeddings. It allows efficient similarity search operations on high-dimensional vector data.

Usage example:

```python
from langchain_gridgain.vectorstores import GridGainVectorStore

# Initialize GridGainVectorStore
def initialize_vector_store(client, embedding_model)-> GridGainVectorStore:
    try:
        vector_store = GridGainVectorStore(
            cache_name="vector_cache",
            embedding=embedding_model,
            client=client
        )
        logger.info("GridGainVectorStore initialized successfully.")
        return vector_store
    except Exception as e:
        logger.error(f"Failed to initialize GridGainVectorStore: {e}")
        raise

# Add texts to the vector store
texts = [
    "The latest MacBook Pro offers exceptional performance for video editing.",
    "Dell XPS 15 is a powerful Windows laptop suitable for creative professionals.",
    "ASUS ROG Zephyrus G14 provides a balance of portability and gaming performance."
]
metadatas = [{"id": "tech_review_1"}, {"id": "tech_review_2"}, {"id": "tech_review_3"}]

vector_store.add_texts(texts=texts, metadatas=metadatas)

# Perform similarity search
query = "What's a good laptop for video editing?"
results = vector_store.similarity_search(query, k=2)

for doc in results:
    print(f"Content: {doc.page_content}")
    print(f"Metadata: {doc.metadata}")
    print("---")

# Clear the vector store
vector_store.clear()
```

## Documentation

For an up-to-date documentation, see the [GridGain Docs](https://www.gridgain.com/docs/extensions/vector/langchain).

## Example

For a comprehensive, real-world example of how to use this package, please refer to the following GitHub repository:

[GG Langchain Demo](https://github.com/GridGain-Demos/gg8_langchain_demo)

gg8_langchain_demo is a demonstration project that showcases the integration of GridGain/Apache Ignite with LangChain, using the custom langchain-gridgain package. This project provides examples of how to use GridGain as a backend for various LangChain components, focusing on a laptop recommendation system.