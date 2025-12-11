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
<img width="330" height="393" alt="image" src="https://github.com/user-attachments/assets/cdc6a497-3eb5-4786-b006-5b7b87ce59ec" />

---
## Requirements

- Python 3.10+
- Install dependencies:

pip install -r requirements.txt

---

## Clone the Project

git clone https://github.com/<your-repo>/code_review_agent.git
cd code_review_agent

## Run the Server

Start FastAPI:

uvicorn app.main:app --reload --port 8000
![WhatsApp Image 2025-12-12 at 00 59 47_b238d1e2](https://github.com/user-attachments/assets/85e7e460-01b2-4093-995e-44fe03c241e0)


Open Swagger UI:

http://localhost:8000/docs

![WhatsApp Image 2025-12-12 at 01 01 40_693d7f47](https://github.com/user-attachments/assets/3ee7da81-392a-4121-b2ec-6b828b08b4be)


---

# How to Use the Workflow Engine

## 1. Create a Sample Graph

POST /graph/create/sample
![WhatsApp Image 2025-12-12 at 00 55 10_f3c2f30e](https://github.com/user-attachments/assets/27621132-baee-4b8c-b521-0cb07a85489e)

Example response:

{ "graph_id": "<id>" }
---

## 2. Run the Workflow

POST /graph/run

Example request body:

{
  "graph_id": "<id>",
  "initial_state": {
  "code": "def foo():\n print("hello")\n # TODO: fix",
  "threshold": 80
  }
}

Example response:

{ "run_id": "<id>" }

![WhatsApp Image 2025-12-12 at 00 57 28_1e807321](https://github.com/user-attachments/assets/aa852ee3-5048-4ee6-90c1-225cd35d4340)

---

## 3. Get Workflow State

GET /graph/state/<run_id>


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

![WhatsApp Image 2025-12-12 at 01 03 24_750628c0](https://github.com/user-attachments/assets/88fbfd2a-dbd7-4f2a-aad9-56fb4b63ca31)


![WhatsApp Image 2025-12-12 at 01 02 44_64500e64](https://github.com/user-attachments/assets/beace960-ea44-447e-9fe0-f2d83eb5e0b5)

---
This project demonstrates a production-ready, extensible mini workflow engine built from scratch — showcasing my ability to design agentic architectures, build clean backend systems, and translate complex logic into modular, testable code.
