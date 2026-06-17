# SQL-agent - Intelligent Database Querying Pipeline

SQL-agent is a robust, local-first conversational agent designed to interact seamlessly with SQL databases. Built using LangChain and powered by offline Ollama models, it processes natural language questions, intelligently navigates database schemas, double-checks its own queries, and fetches precise answers without requiring an internet connection for the LLM.

It connects to your database, automatically extracts relevant schema information, constructs syntactically correct SQL queries, executes them securely, and synthesizes the results into human-readable answers.

## Key Features
* **Zero-Shot SQL Generation** — Ask questions in plain English; no prompt engineering required.
* **Fully Offline Inference** — Powered by local Ollama models (like `llama3`), ensuring complete data privacy and no API costs.
* **Intelligent ReAct Loop** — The agent "thinks" before it acts, queries available tables, reads schemas, and self-corrects if a query fails.
* **LangSmith Observability** — Full integration with LangSmith for beautiful, step-by-step traces of the agent's internal reasoning.
* **Lightning Fast Setup** — Uses `uv` for blazing fast Python dependency management.

## Project Structure
```text
sql-agent/
├── agent.py              # Main agent execution loop and database connection
├── model.py              # LangChain ChatOllama LLM configuration
├── Chinook.db            # Sample SQLite database
├── .env.example          # Template for required environment variables
├── pyproject.toml        # Project dependencies managed by uv
└── README.md             # This documentation
```

## Quick Start

### 1. Installation
Ensure you have `uv` and `ollama` installed on your machine.
```bash
git clone https://github.com/divijaiwanth/sql-agent.git
cd sql-agent
uv sync
```

### 2. Configure Environment
Copy the example environment file:
```bash
cp .env.example .env
```
Open `.env` and fill in your LangSmith keys if you want to enable tracing:
* `LANGCHAIN_TRACING_V2=true`
* `LANGCHAIN_API_KEY=your_key`
* `LANGCHAIN_PROJECT=sql-agent`

### 3. Setup Local LLM
Ensure Ollama is running on your machine, and pull the required model (we use `llama3` by default, but you can change this in `model.py`):
```bash
ollama pull llama3
```

### 4. Run the Agent
Execute the agent to see it solve the sample question:
```bash
uv run python agent.py
```

## Technology Stack
| Component | Technology |
| --- | --- |
| **Agent Framework** | LangChain / LangGraph (`create_sql_agent`) |
| **Offline LLM Inference** | Ollama (`llama3`) |
| **Database Engine** | SQLite |
| **Observability & Tracing** | LangSmith |
| **Package Management** | `uv` |
| **Core Language** | Python |

## How It Works

1. **Initialization**
   The application connects to `Chinook.db` using LangChain's `SQLDatabase` utility and instantiates the `ChatOllama` model.
2. **Schema Discovery**
   When asked a question, the agent uses built-in tools to list all available tables (`sql_db_list_tables`) and read the schema of relevant tables (`sql_db_schema`).
3. **Query Construction & Validation**
   The agent formulates an SQL query. Before executing, it uses its reasoning loop to verify there are no syntax errors.
4. **Execution & Synthesis**
   The agent runs the query against the database (`sql_db_query`), observes the raw data output, and synthesizes a natural language final answer.

## Why SQL-agent?
SQL-agent showcases strong end-to-end AI engineering skills — from handling database integrations to building a complete, scalable, and fully local agentic workflow. 

It combines:
* Large Language Model reasoning (ReAct)
* Tool-calling and arbitrary code execution safety
* Seamless environment and dependency management
* Advanced LLM observability using LangSmith

into one complete production-ready pipeline.

## ❤️ Made With Passion
Made with ❤️ by Divi Jaiwanth
