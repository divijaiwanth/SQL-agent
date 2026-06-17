# SQL-agent — Intelligent Database Querying Pipeline
 
SQL-agent is a local-first conversational agent for SQL databases. Built with LangChain and powered by offline Ollama models, it takes natural language questions, explores the database schema on its own, constructs and validates SQL queries, and returns accurate answers, all without sending any data over the internet.
 
It connects to your database, automatically extracts relevant schema information, constructs syntactically correct SQL queries, executes them securely, and synthesizes the results into a human-readable answer.
 
## Key Features
 
- **Zero-Shot SQL Generation** — Ask questions in plain English, no prompt engineering required.
- **Fully Offline Inference** — Powered by local Ollama models (e.g. `llama3`), ensuring full data privacy and zero API cost.
- **Intelligent ReAct Loop** — The agent reasons before acting: it lists tables, reads schemas, constructs a query, and self-corrects on failure.
- **LangSmith Observability** — Full integration with LangSmith for step-by-step traces of the agent's internal reasoning.
- **Lightning Fast Setup** — Uses `uv` for fast, reliable Python dependency management.
## Project Structure
 
```
sql-agent/
├── agent.py              # Main agent execution loop and database connection
├── model.py              # LangChain ChatOllama LLM configuration
├── test.py                # Batch evaluation harness (25 test questions, CSV output)
├── test_results.csv       # Pre-run evaluation results (see Evaluation section below)
├── Chinook.db             # Sample SQLite database
├── .env.example           # Template for required environment variables
├── pyproject.toml         # Project dependencies managed by uv
└── README.md              # This documentation
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
 
- `LANGCHAIN_TRACING_V2=true`
- `LANGCHAIN_API_KEY=your_key`
- `LANGCHAIN_PROJECT=sql-agent`
### 3. Setup Local LLM
 
Ensure Ollama is running on your machine, and pull the required model (default is `llama3`, configurable in `model.py`):
 
```bash
ollama pull llama3
```
 
### 4. Run the Agent
 
```bash
uv run python agent.py
```
 
## Technology Stack
 
| Component | Technology |
|---|---|
| Agent Framework | LangChain (`create_sql_agent`) |
| Offline LLM Inference | Ollama (`llama3`) |
| Database Engine | SQLite |
| Observability & Tracing | LangSmith |
| Package Management | `uv` |
| Core Language | Python |
 
## How It Works
 
1. **Initialization** — The application connects to `Chinook.db` using LangChain's `SQLDatabase` utility and instantiates the `ChatOllama` model.
2. **Schema Discovery** — When asked a question, the agent lists all available tables (`sql_db_list_tables`) and reads the schema of relevant ones (`sql_db_schema`).
3. **Query Construction & Validation** — The agent formulates a SQL query and reasons through it before executing, checking for syntax errors.
4. **Execution & Synthesis** — The agent runs the query (`sql_db_query`), observes the raw output, and synthesizes a natural language answer.
## Evaluation
 
The agent was tested against 25 natural language questions spanning five difficulty tiers on the Chinook dataset, using `test.py`. Each question was run once (no retries) and graded by hand against known correct answers.
 
A completed run is already included in this repo at [`test_results.csv`](./test_results.csv), so you can inspect the exact questions, agent answers, timings, and errors without re-running anything yourself.
 
| Tier | Description | Accuracy |
|---|---|---|
| 1 | Simple lookups (single table) | 5/5 (100%) |
| 2 | Single join | 3/5 (60%) |
| 3 | Multi-table joins | 2/5 (40%) |
| 4 | Aggregation + filtering | 3/5 (60%) |
| 5 | Ambiguous / open-ended natural language | 2/5 (40%) |
| **Overall** | | **15/25 (60%)** |
 
**Key findings:**
 
- The agent is fully reliable on direct, single-table lookups and simple joins.
- Most failures stemmed from a ReAct output-parsing issue, the local LLM occasionally emitted a final answer and a tool action in the same response, which LangChain's parser rejects. This accounted for 5 of the 8 failed questions.
- One failure was a genuine query logic bug: the model joined two tables on unrelated columns, producing a syntactically valid but semantically incorrect query.
- On ambiguous questions (e.g. "what's popular right now?"), the agent sometimes picked an arbitrary ranking metric instead of asking for clarification, an expected limitation of zero-shot agents on underspecified prompts.
**Planned improvements:**
 
- Add `handle_parsing_errors=True` to the agent executor to recover from output-parsing failures automatically.
- Evaluate stronger instruction-following local models (e.g. `llama3.1`) for ReAct format adherence.
- Add a clarification step for ambiguous queries before query generation.
Want to reproduce or extend these results? Run the evaluation yourself:
 
```bash
uv run python test.py
```
 
This regenerates `test_results.csv` with fresh answers, timings, and any errors, useful if you change the model, prompt, or add your own test questions.
 
## Why SQL-agent?
 
SQL-agent demonstrates end-to-end AI engineering across database integration, agentic reasoning, and systematic evaluation, combining:
 
- LLM reasoning via the ReAct loop
- Tool-calling with schema discovery and query validation
- Local, fully private inference with zero API cost
- LLM observability via LangSmith
- A repeatable evaluation harness for measuring and improving agent reliability
into a complete, locally-run, and rigorously tested pipeline.

## ❤️ Made With Passion
Made with ❤️ by Divi Jaiwanth
