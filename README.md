🚀 Code Review Mini-Agent – Mini Workflow Engine (FastAPI)

A compact FastAPI project implementing a minimal workflow/agent engine (backend only).
This engine demonstrates:

Nodes as Python functions that read/modify shared state

Directed edges, branching, and looping using simple state directives

A tool registry for reusable utility functions

Async workflow execution

WebSocket support for real-time log streaming

This project fulfills the AI Engineering Intern Assignment by showcasing workflow orchestration, backend architecture, and agent-style state transitions.

📁 Project Structure
app/
  main.py                 # FastAPI application + endpoints
  engine/
      graph.py            # Graph engine, Node, executor logic
  tools/
      code_tools.py       # Simple rule-based analysis tools
  workflows/
      code_review.py      # Code Review workflow definition
  storage/
      memory_store.py     # In-memory graph/run storage
requirements.txt
README.md

📸 Example Screenshot

(Add your folder-structure screenshot here)
![Project Structure](images/structure.jpg)

📦 Requirements

Python 3.10+

Install dependencies:

pip install -r requirements.txt

▶️ Run the Server

Start FastAPI using Uvicorn:

uvicorn app.main:app --reload --port 8000


📸 (Add terminal screenshot)
![Terminal Running](images/terminal.jpg)

Now visit:

👉 http://localhost:8000/docs

📸 (Add Swagger screenshot)
![Swagger UI](images/swagger.jpg)

🧪 How to Use the Workflow Engine
1️⃣ Create a Sample Graph
POST /graph/create/sample


Response:

{ "graph_id": "<id>" }


📸
![Create Graph](images/create_graph.jpg)

2️⃣ Start a Workflow Run
POST /graph/run


Example Body:

{
  "graph_id": "<id>",
  "initial_state": {
    "code": "def foo():\n    print(\"hello\")\n    # TODO: fix",
    "threshold": 80
  }
}


Response:

{ "run_id": "<id>" }


📸
![Run Workflow](images/run_graph.jpg)

3️⃣ Get Workflow State & Logs
GET /graph/state/<run_id>


Response Example:

{
  "state": {
    "functions": ["foo"],
    "function_count": 1,
    "complexity": 3,
    "issues": ["has_todo", "debug_prints"],
    "issue_count": 2,
    "suggestions": ["remove debug prints / address TODOs"],
    "quality_score": 107
  },
  "log": [
    "starting run at node: extract_functions",
    "running node: extract_functions",
    "running node: check_complexity",
    "running node: detect_issues",
    "running node: suggest_improvements",
    "completed"
  ],
  "status": "completed"
}


📸
![Get State](images/get_state.jpg)

4️⃣ Stream Logs (Optional)

Use any WebSocket client:

ws://localhost:8000/ws/<run_id>


📸 (Optional WebSocket screenshot)
![WS Logs](images/ws_logs.jpg)

🧠 What This Demo Shows
✔️ Clean, modular Python backend
✔️ Workflow graph + state machine implementation
✔️ Branching & looping via _goto directive
✔️ Async-friendly node execution
✔️ Real-time log streaming
✔️ Easily extensible architecture (add nodes, agents, tools)
🚀 Possible Improvements (If More Time)

SQLite/Postgres persistent storage

Store graphs as JSON specs

Retry logic, scheduling, observability

Multi-tenant authenticated workflows

More advanced code analysis tools
