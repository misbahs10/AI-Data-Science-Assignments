# ✦ NOVA — AI Task Manager Agent

An AI-powered task management application built with **Python, Streamlit, Groq LLM, and SQLite**. NOVA allows users to manage their daily tasks using natural language instructions through an intelligent AI agent.

Instead of manually managing every task, users can simply communicate with NOVA to create tasks, view their task list, update completion status, delete tasks, and calculate mathematical expressions.

---

## 🚀 Project Overview

NOVA is an AI Task Manager Agent that combines Large Language Models (LLMs) with Python-based tools to perform real-world task management operations.

The application provides an interactive dashboard where users can:

- Create tasks using natural language.
- Assign task priorities: High, Medium, or Low.
- Set task descriptions and due dates.
- View all saved tasks.
- Mark tasks as completed.
- Delete existing tasks.
- Track task statistics and progress.
- Calculate mathematical expressions through the AI assistant.

NOVA follows a tool-calling architecture in which the LLM identifies the user's intention, selects the appropriate tool, executes the operation, and generates a natural-language response.

---

## ✨ Key Features

### 1. AI-Powered Task Management
- Natural language task creation.
- Automatic tool selection using Groq LLM.
- Task creation with title, description, due date, and priority.
- Task listing and filtering.
- Task completion and deletion.

### 2. Interactive Dashboard
- Clean and responsive Streamlit interface.
- Light lavender and soft blue visual theme.
- Overview dashboard with task statistics.
- Recent tasks section.
- Quick navigation between application pages.
- AI agent status indicator.

### 3. AI Assistant
- Conversational interface.
- Natural language instructions.
- Tool-based task operations.
- Mathematical calculations.
- Chat history during the active application session.

### 4. SQLite Database
- Persistent local task storage.
- Automatic database initialization.
- Structured task records.
- Task status tracking.
- SQL-based CRUD operations.

### 5. Task Analytics
- Total tasks.
- Pending tasks.
- Completed tasks.
- Task filtering by completion status.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Groq API | LLM inference |
| GPT OSS 20B | AI agent model |
| Streamlit | Interactive web application |
| SQLite | Task database |
| Pandas | Data handling dependency |
| Python-dotenv | Environment variable management |
| HTML & CSS | Dashboard styling |

---

## 🧠 How NOVA Works

NOVA uses an AI tool-calling workflow.

1. **User Input:** The user sends a natural language instruction.
2. **LLM Processing:** Groq's language model interprets the request.
3. **Tool Selection:** The agent selects the appropriate Python function.
4. **Tool Execution:** The selected function performs the requested operation.
5. **Database Operation:** Task information is retrieved or updated in SQLite when required.
6. **AI Response:** The agent returns a human-readable response.

### Agent Workflow

```text
          User Instruction
                 |
                 v
          Streamlit UI
                 |
                 v
             AI Agent
                 |
                 v
          Groq LLM
                 |
                 v
          Tool Selection
                 |
       +---------+---------+
       |         |         |
       v         v         v
   Create     List      Calculate
    Task      Tasks
       |         |
       v         v
    SQLite    SQLite
       |
       v
   Complete / Delete
       |
       v
   Tool Response
       |
       v
    AI Response
       |
       v
    User Interface
```

---

## 📁 Project Structure

```text
ai-task-agent/
│
├── agent/
│   └── main.py
│
├── database/
│   ├── db.py
│   └── tasks.db
│
├── tools/
│   ├── task_tool.py
│   ├── calculator_tool.py
│   └── search_tool.py
│
├── app.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

**Folder Description**

| File / Folder | Description |
|---|---|
| `agent/main.py` | Core AI agent and tool-calling logic |
| `database/db.py` | SQLite database initialization and operations |
| `database/tasks.db` | Local database containing saved tasks |
| `tools/task_tool.py` | Task creation, listing, completion, deletion, and summary functions |
| `tools/calculator_tool.py` | Mathematical calculation tool |
| `tools/search_tool.py` | Web search utility |
| `app.py` | Streamlit application and dashboard |
| `requirements.txt` | Project dependencies |
| `.env` | Local API key configuration |
| `.gitignore` | Excludes sensitive and unnecessary files |

---

## ⚙️ Installation & Setup

### Prerequisites

Make sure you have:

- Python 3.10 or later.
- Git.
- A Groq API key.

### Step 1: Clone the Repository

```bash
git clone https://github.com/misbahs10/Python-ML-Lab/ai-task-agent.git
```

Navigate to the project directory:

```bash
cd Python-ML-Lab/ai-task-agent
```

### Step 2: Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment on Windows:

```powershell
venv\Scripts\activate
```

For macOS/Linux:

```bash
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create a `.env` file in the `ai-task-agent` directory.

Add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Get your API key from:

https://console.groq.com/keys

**Important:** Never upload your `.env` file or expose your API key publicly.

### Step 5: Run the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your browser, usually at:

```text
http://localhost:8501
```

---

## 💬 Example AI Instructions

Users can interact with NOVA using natural language.

### Create a Task

```text
Create a high priority task titled
"Complete AI Assignment"
with description "Finish my AI agent project"
and due date 2026-11-25.
```

### View Tasks

```text
Show all my tasks.
```

### View Pending Tasks

```text
Show all my pending tasks.
```

### Complete a Task

```text
Mark task ID 1 as completed.
```

### Delete a Task

```text
Delete task ID 1.
```

### Task Summary

```text
Give me a summary of my tasks.
```

### Calculate

```text
Calculate 250 * 15.
```

---

## 🗄️ Database Schema

NOVA uses SQLite to store task information.

### Tasks Table

| Column | Data Type | Description |
|---|---|---|
| id | INTEGER | Unique task ID |
| title | TEXT | Task title |
| description | TEXT | Task description |
| due_date | TEXT | Task deadline |
| priority | TEXT | Low, Medium, or High |
| status | TEXT | Pending or Completed |
| created_at | TIMESTAMP | Task creation timestamp |

The database is initialized automatically when the application starts.

---

## 🔐 Security & Configuration

- API credentials are stored in environment variables.
- `.env` is excluded from version control.
- SQLite queries use parameterized statements.
- Mathematical expressions are evaluated using a restricted AST-based calculator rather than unrestricted Python evaluation.
- Application configuration is separated from task database operations.

---

## ☁️ Deployment

NOVA is designed to run as a Streamlit web application.

For deployment using Streamlit Community Cloud:

1. Push the project to a GitHub repository.
2. Open https://share.streamlit.io/
3. Connect your GitHub account.
4. Select the repository and branch.
5. Set the application entry point to:

```text
ai-task-agent/app.py
```

6. Configure the `GROQ_API_KEY` through Streamlit Secrets.
7. Deploy and test the application.

**Deployment note:** The application must be configured to read the Groq API key from `st.secrets` in the cloud environment. Local `.env` files are not automatically available on Streamlit Community Cloud.

SQLite storage on Streamlit Community Cloud should be treated as temporary unless a persistent external database or storage solution is configured.

---

## 🔮 Future Improvements

- Long-term conversational memory.
- User authentication and personalized task management.
- Cloud database integration.
- Task reminders and notifications.
- Task editing functionality.
- Advanced productivity analytics.
- Multi-agent task planning.
- Integration with calendar applications.
- Deployment with persistent cloud storage.

---

## 🎯 Learning Outcomes

Through this project, I practiced:

- Building AI agents with LLM tool calling.
- Integrating Groq API with Python.
- Designing modular Python applications.
- Implementing SQLite database operations.
- Developing interactive dashboards with Streamlit.
- Using natural language to trigger real application actions.
- Managing API credentials and project dependencies.

---

## 👩‍💻 Author

**Misbah Sajjad**

AI & Data Science Learner | Python Developer

- GitHub: https://github.com/misbahs10/Python-ML-Lab/tree/main/ai-task-agent
- LinkedIn: https://www.linkedin.com/in/misbahsajjad23/

---

## ⭐ Support

If you find this project interesting, consider giving the repository a star!

**Built with Python, Streamlit, SQLite, and Groq AI.**

*Turning natural language into real task management actions.*