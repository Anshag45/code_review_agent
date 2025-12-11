from fastapi import FastAPI, WebSocket, BackgroundTasks, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import uuid
import asyncio
from app.engine.graph import Graph
from app.storage.memory_store import MemoryStore
from app.workflows.code_review import build_code_review_graph


app = FastAPI(title="Mini Workflow Engine - Code Review (Intern)")

store = MemoryStore()

class CreateGraphRequest(BaseModel):
    graph: Dict[str, Any]

class RunGraphRequest(BaseModel):
    graph_id: str
    initial_state: Dict[str, Any]

@app.post("/graph/create")
async def create_graph(req: CreateGraphRequest):
    graph_id = str(uuid.uuid4())
    graph = Graph.from_dict(req.graph)
    store.save_graph(graph_id, graph)
    return {"graph_id": graph_id}

@app.post("/graph/create/sample")
async def create_sample_graph():
    graph_obj = build_code_review_graph()
    graph_id = str(uuid.uuid4())
    store.save_graph(graph_id, graph_obj)
    return {"graph_id": graph_id}

@app.post("/graph/run")
async def run_graph(req: RunGraphRequest, background_tasks: BackgroundTasks):
    graph = store.get_graph(req.graph_id)
    if not graph:
        raise HTTPException(status_code=404, detail="Graph not found")
    run_id = str(uuid.uuid4())
    store.create_run(run_id, {"state": req.initial_state, "log": [], "status":"running"})
    # run in background
    background_tasks.add_task(graph.execute, req.initial_state, run_id, store)
    return {"run_id": run_id}

@app.get("/graph/state/{run_id}")
async def get_state(run_id: str):
    run = store.get_run(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return run

@app.websocket("/ws/{run_id}")
async def websocket_endpoint(websocket: WebSocket, run_id: str):
    await websocket.accept()
    try:
        while True:
            run = store.get_run(run_id)
            if run is None:
                await websocket.send_json({"error":"run not found"})
                break
            # send latest log entry
            log = run.get("log", [])
            await websocket.send_json({"state": run["state"], "log": log, "status": run.get("status","")})
            if run.get("status") in ("completed","failed"):
                break
            await asyncio.sleep(1.0)
    finally:
        await websocket.close()
