# SQL Agent

A lightweight Python project for turning natural-language questions into safe SQL queries and executing them against a database.

## Features

- Safe SQL validation to block destructive statements
- SQL execution helper for SELECT queries
- Simple memory/history support for conversation context
- LangGraph-based workflow scaffolding for agent-style execution
- Basic gateway client integration for LLM-based SQL generation

## Project Structure

- `src/` – core application modules
  - `app.py` – main application entry point
  - `safety.py` – SQL validation helpers
  - `sql_tools.py` – SQL execution helpers
  - `memory.py` – memory and conversation history helpers
  - `graph.py` – LangGraph workflow logic
  - `tiger_gateway_client.py` – LLM gateway client
- `tests/` – pytest test suite
- `data/` – sample CSV data
- `database/` – schema and loading scripts

## Setup

1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
   On Windows PowerShell:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set any required environment variables for the LLM gateway, if needed.

## Running the App

Run the interactive app:

```bash
python -m src.app
```

## Running Tests

Run the test suite with:

```bash
pytest
```

## Notes

- The project currently focuses on safe read-only SQL execution.
- The LLM gateway integration is optional and can fall back to simple defaults when configuration is not provided.
