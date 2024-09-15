# uc-rag-chatbot

## Bearchat

**Bearchat** is a course assistant RAG chatbot developed as a proof of concept for the University of Cincinnati's Lindner College of Business. The RAG (Retrieval-Augmented Generation) chatbot is a sophisticated conversational AI system designed to provide accurate and contextually relevant responses by leveraging advanced search and language models.

This tool is designed to provide students with tailored support for their coursework queries. By leveraging UC’s proprietary documents and instructors' course manuals, Bearchat generates precise, context-specific responses, enhancing the academic experience and streamlining access to essential information. Its integration with the university's academic resources ensures that students receive relevant and timely assistance, ultimately fostering a more efficient and informed learning environment.

It integrates **Azure AI Search** and **OpenAI's GPT-4-o** to handle queries based on both a knowledge base and historical interaction memory.

## Frontend

For the proof of concept (POC), a Q&A interface was developed using **Streamlit**.

- **Interface:** Built with Streamlit, providing a user-friendly interface for interacting with the chatbot.
- **Document Upload:** Users can upload documents via the Streamlit interface. The file is sent to an Azure Function for processing.
- **Question Handling:** Users can ask questions, which are sent to an Azure Function for generating answers.
- **Interaction History:** The app provides a simple interface for users to ask questions. Questions and answers are stored and displayed in the app interface, ensuring users can see a history of their interactions.

## Backend

### Azure Functions

The backend utilizes Azure Functions, with the main entry point being the Function App, which registers the `DataProcessing` and `userQuery` blueprints.

1. **Document Processing:** Processes uploaded documents (e.g., PDFs), extracts text, chunks it into smaller pieces, embeds the text using OpenAI's embedding models, and indexes it in Azure Search.
2. **User Query Handling:** Handles user queries, retrieves relevant documents from the index, generates a response using OpenAI's GPT model, and provides an answer.

## Architecture

![Architecture Diagram](https://raw.githubusercontent.com/ajayiitrlearner/uc-rag-chatbot/main/ajay_rag/chatbot-backend/architecture.png)

The chatbot system is composed of several key components, divided into two main categories: **Indexing** and **Retrieval**.

### Indexing

Indexing involves preparing and storing data so that it can be efficiently retrieved later. This process includes:

1. **Document Processing**
   - **Component:** `DataProcessing_blueprint.cpython-311.pyc`
   - **Function:** Processes uploaded PDF documents and extracts text.

2. **Chunking Process**
   - **Purpose:** Break large documents into manageable pieces.
   - **Tools Used:** `RecursiveCharacterTextSplitter` from `langchain_text_splitters`.
   - **Process:**
     - The documents are read, and text content is extracted using PyPDF2.
     - The text is chunked into manageable sizes for embedding.
     - Define separators (sentence endings and word breaks).
     - Concatenate document text.
     - Split text into chunks of ~300 characters with a 20-character overlap.

3. **Embedding Process**
   - **Purpose:** Convert text chunks into vector representations.
   - **Tool Used:** OpenAI Embedding Model (`text-embedding-3-small`).
   - **Process:**
     - Clean text to remove unwanted characters.
     - Generate embeddings using OpenAI's API.

4. **Indexing Process**
   - **Purpose:** Store embedded text chunks in a searchable index.
   - **Tool Used:** Azure AI Search.
   - **Process:**
     - Create unique IDs for each chunk.
     - Store chunk content, embedding, and page number.

### Other Core Components

- **OpenAI API:** Used for generating responses and embeddings.
- **Embedding Service:** Generates vector embeddings for the documents and queries.
- **Chat Completion Service:** Generates natural language responses based on the provided context and user queries.
- **Azure Blob Storage:** Stores the uploaded documents temporarily for processing.

## Azure Configurations

1. **Storage:** A storage container to store function and AI search.
2. **Azure Functions App:** The core of the RAG chatbot.

### HTTP Trigger Functions

- **DataProcessing Function:** Handles file uploads, processes documents, and indexes them in Azure AI Search.
- **UserQuery Function:** Handles user queries, retrieves relevant documents, and generates responses using GPT-4-o.

### Azure AI Search

Includes built-in vector search capabilities, which allow for similarity searches using vector representations of data.

- **Knowledge Base Index:** Stores and retrieves knowledge documents that provide answers to user queries.
- **Memory Index:** Stores and retrieves past interactions (queries and responses) to provide contextual answers.

In both indexes, vector profile configurations are as follows:

- **Vector profile kind:** `hnsw` (Hierarchical Navigable Small World graph).
- **Bi-directional link count (m):** 4.
- **efConstruction:** 400 (controls the accuracy and construction time of the index).
- **efSearch:** 500 (controls the accuracy and speed of the search query).
- **Similarity metric:** cosine (used to measure the similarity between vectors).

## Retrieval

Retrieval involves querying indexed data to find relevant information and generating responses based on that information.

- **Query Handling:** User queries are vectorized using the same embedding model.
- **Relevant documents** are retrieved using Azure Search.
- **Prompt Engineering** to extract the required response based on context, conversation history, and language model.
- **OpenAI GPT-4 model** generates responses based on retrieved documents.

### Prompt Engineering

![ Prompting](https://raw.githubusercontent.com/ajayiitrlearner/uc-rag-chatbot/main/ajay_rag/chatbot-backend/prompts.png)

Prompts for GPT-4-o are structured as follows:

1. Classifies the query to check if it's a general or specific question using `classify_self_questions_llm`.
2. Retrieves relevant documents from the index using `get_relevant_documents`.
3. Generates a response based on the retrieved documents and the query using `final_response_from_llm`.
4. If the query is classified as a general question, it responds with a predefined answer using `self_response_from_llm`.

## Conclusion

The RAG chatbot represents a cutting-edge integration of AI and search technologies, offering highly relevant and contextually rich responses. By combining Azure Cognitive Search with OpenAI's language models and embedding techniques, the chatbot delivers high-quality answers based on both static knowledge and dynamic interaction history.

With upcoming enhancements, including custom AI avatars and lip-synced, voice-enabled interactions, the chatbot will provide an even more personalized and immersive user experience, bridging the gap between static information retrieval and dynamic, human-like communication.
