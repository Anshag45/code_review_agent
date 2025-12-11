# Code Review Mini-Agent - Mini Workflow Engine (FastAPI)

This is a compact FastAPI project implementing a small workflow/agent engine (backend only).
It demonstrates:
- Nodes as Python functions that read/modify shared state
- Edges, branching, and looping via simple state directives
- Tool registry for reusable functions
- Async execution and a WebSocket endpoint to stream run state/logs

## Structure
- `app/main.py` - FastAPI app & endpoints
- `app/engine/graph.py` - Graph + Node + executor logic
- `app/tools/code_tools.py` - Simple rule-based tools used by nodes
- `app/workflows/code_review.py` - Sample Code Review workflow builder
- `app/storage/memory_store.py` - In-memory storage for graphs & runs

## Requirements
- Python 3.10+
- Install:
  ```
  pip install -r requirements.txt
  ```

## Run
1. Start the server:
   ```
   uvicorn app.main:app --reload --port 8000
   ```
2. Create sample graph:
   ```
   POST /graph/create/sample
   ```
   Response: `{ "graph_id": "<id>" }`
3. Start a run:
   ```
   POST /graph/run
   {
     "graph_id": "<id>",
     "initial_state": { "code": "def foo():\n    print(\"hello\")\n    # TODO: fix", "threshold": 80 }
   }
   ```
   Response: `{ "run_id": "<id>" }`
4. Stream logs via WebSocket:
   ```
   ws://localhost:8000/ws/<run_id>
   ```
5. Query run state:
   ```
   GET /graph/state/<run_id>
   ```

## What this demo shows
- Clean, modular Python code
- Async-friendly node execution
- Branching and looping via a simple `_goto` state directive
- How to structure a small workflow engine suitable for expansion

## Improvements (if more time)
- Persistent storage (SQLite/Postgres)
- Pluggable node serialization (store graphs as JSON/spec)
- Authentication & multi-tenant runs
- More advanced scheduling, retries, observability
