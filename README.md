# Code Review Mini-Agent - Mini Workflow Engine (FastAPI)

This is a compact FastAPI project implementing a minimal workflow/agent engine (backend only).  
It demonstrates:

- Nodes as Python functions that read and modify shared state  
- Directed edges, branching, and looping  
- A tool registry for reusable functions  
- Async execution  
- Optional WebSocket streaming of logs  

This project fulfills the AI Engineering Intern Assignment by showcasing workflow orchestration, backend architecture, and agent-style state transitions.

---

## Project Structure

app/
main.py
engine/
graph.py
tools/
code_tools.py
workflows/
code_review.py
storage/
memory_store.py
requirements.txt
README.md
images/

yaml
Copy code

(Add screenshot here)  
![Project Structure](images/structure.jpg)

---

## Requirements

- Python 3.10+
- Install dependencies:

pip install -r requirements.txt

yaml
Copy code

---

## Run the Server

Start FastAPI:

uvicorn app.main:app --reload --port 8000

yaml
Copy code

(Add terminal screenshot)  
![Terminal](images/terminal.jpg)

Open Swagger UI:

http://localhost:8000/docs

(Add screenshot)  
![Swagger](images/swagger.jpg)

---

# How to Use the Workflow Engine

## 1. Create a Sample Graph

POST /graph/create/sample

yaml
Copy code

Example response:

{ "graph_id": "<id>" }

yaml
Copy code

(Add screenshot)  
![Create Graph](images/create_graph.jpg)

---

## 2. Run the Workflow

POST /graph/run

css
Copy code

Example request body:

{
"graph_id": "<id>",
"initial_state": {
"code": "def foo():\n print("hello")\n # TODO: fix",
"threshold": 80
}
}

yaml
Copy code

Example response:

{ "run_id": "<id>" }

yaml
Copy code

(Add screenshot)  
![Run Workflow](images/run_graph.jpg)

---

## 3. Get Workflow State

GET /graph/state/<run_id>

lua
Copy code

Example output:

{
"state": {
"functions": ["foo"],
"function_count": 1,
"complexity": 3,
"issues": ["has_todo", "debug_prints"],
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

yaml
Copy code

(Add screenshot)  
![Get State](images/get_state.jpg)

---

## What This Demo Shows

- Clean, modular Python backend  
- Workflow engine and state machine design  
- Branching and looping with `_goto`  
- Async execution  
- Real-time logging option  

---

## Improvements (If More Time)

- Persistent database storage  
- JSON-spec workflow definitions  
- Failure handling and retries  
- Authentication  
- Better observability  
