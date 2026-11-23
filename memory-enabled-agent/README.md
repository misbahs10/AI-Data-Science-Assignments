# 🧠 Memory-Enabled AI Agent

A context-aware AI assistant developed using Python, Streamlit, Groq, SQLite, and FastEmbed. This project demonstrates how AI agents can maintain short-term conversation history, store persistent long-term memories, and retrieve relevant information through semantic search to generate personalized responses.

## ✨ Key Features

- **Short-Term Memory:** Maintains recent conversation history for contextual responses.
- **Long-Term Memory:** Stores persistent user information using SQLite.
- **Semantic Memory Retrieval:** Uses FastEmbed embeddings and cosine similarity to retrieve relevant memories.
- **Memory Management:** Supports adding, searching, updating, and deleting stored memories.
- **Automatic Embedding Indexing:** Generates embeddings when new memories are saved or existing memories are updated.
- **Conversation Management:** Supports creating and switching between multiple conversations.
- **Context-Aware AI Responses:** Combines conversation history and relevant long-term memories before generating responses.
- **Interactive Streamlit UI:** Provides a chat interface with conversation and memory management features.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application development |
| Streamlit | Interactive web interface |
| Groq API | Large Language Model integration |
| SQLite | Persistent memory and conversation storage |
| FastEmbed | Text embedding generation |
| BAAI/bge-small-en-v1.5 | Semantic embedding model |
| Python-dotenv | Environment variable management |

## 🏗️ Project Architecture

The application consists of four main components:

1. **User Interface:** Streamlit handles user interaction, chat messages, conversations, and memory management.
2. **Memory Management:** Short-term and long-term memory modules manage conversation history and persistent user information.
3. **Semantic Retrieval:** FastEmbed generates vector embeddings, while cosine similarity identifies relevant memories.
4. **LLM Integration:** Groq generates responses using the current message, conversation history, and retrieved memories.

## 📁 Project Structure

```text
memory-enabled-agent/
│
├── agent/
│   ├── __init__.py
│   ├── llm.py
│   └── prompts.py
│
├── memory/
│   ├── __init__.py
│   ├── database.py
│   ├── short_term.py
│   ├── long_term.py
│   ├── retriever.py
│   └── manager.py
│
├── database/
│   └── .gitkeep
│
├── utils/
│   ├── __init__.py
│   └── helpers.py
│
├── .streamlit/
│   └── config.toml
│
├── app.py
├── config.py
├── init_db.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
│
├── test_database.py
├── test_short_term.py
├── test_long_term.py
├── test_retriever.py
├── test_manager.py
└── test_llm.py
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/misbahs10/AI-Data-Science-Assignments.git
```

### 2. Navigate to the project directory

```bash
cd AI-Data-Science-Assignments/memory-enabled-agent
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

Activate the environment on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file in the project root directory.

Add the following configuration:

```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=openai/gpt-oss-20b
```

Get your API key from the Groq developer console:

https://console.groq.com/

**Security Note:** Never share or upload your actual API key. The `.env` file is excluded from Git through `.gitignore`.

### 6. Initialize the database

```bash
python init_db.py
```

This initializes the SQLite database and creates the required tables.

### 7. Run the application

```bash
streamlit run app.py
```

The application will open in your default web browser.

## 🧪 Testing

Individual test scripts are included to verify the functionality of each major component.

Run the tests from the project root:

```bash
python test_database.py
python test_short_term.py
python test_long_term.py
python test_retriever.py
python test_manager.py
python test_llm.py
```

### Tested Components

- SQLite database initialization and CRUD operations.
- Short-term conversation memory.
- Long-term memory storage and management.
- Semantic memory retrieval.
- Memory manager integration.
- Groq LLM response generation.

## 🔄 Application Workflow

1. The user submits a message through the Streamlit chat interface.
2. The application retrieves recent conversation history from SQLite.
3. The semantic retriever searches stored long-term memories.
4. Relevant memories are selected using embedding similarity.
5. Conversation history and retrieved memories are provided as context to the LLM.
6. Groq generates a context-aware response.
7. User and assistant messages are stored in the database.

## 🔐 Security and Data Management

- API credentials are stored in environment variables.
- `.env` files are excluded from version control.
- SQLite database files are excluded from Git.
- Virtual environments and Python cache files are excluded from Git.
- `.env.example` provides a safe configuration template without exposing credentials.

## 🚀 Future Improvements

- Add a dedicated memory editing and deletion interface.
- Implement memory importance scoring.
- Add conversation export functionality.
- Improve memory deduplication and retrieval ranking.
- Add support for multiple LLM providers.

## 👩‍💻 Author

**Misbah Sajjad**

- GitHub: [misbahs10](https://github.com/misbahs10)
- LinkedIn: [Misbah Sajjad](https://www.linkedin.com/in/misbahsajjad23)

---

*Developed as part of an AI and Data Science assignment focused on building memory-enabled AI agents using Python and modern AI technologies.*