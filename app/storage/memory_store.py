# Very small in-memory store to save graphs and runs
from typing import Dict, Any

class MemoryStore:
    def __init__(self):
        self.graphs = {}
        self.runs = {}

    def save_graph(self, graph_id: str, graph):
        self.graphs[graph_id] = graph

    def get_graph(self, graph_id: str):
        return self.graphs.get(graph_id)

    def create_run(self, run_id: str, run_obj: Dict[str, Any]):
        self.runs[run_id] = run_obj

    def get_run(self, run_id: str):
        return self.runs.get(run_id)

    def append_run_log(self, run_id: str, message: str):
        run = self.runs.get(run_id)
        if run is None:
            return
        run.setdefault("log", []).append(message)

    def update_run_state(self, run_id: str, state: Dict[str, Any]):
        run = self.runs.get(run_id)
        if run is None:
            return
        run["state"] = dict(state)

    def mark_run_completed(self, run_id: str):
        run = self.runs.get(run_id)
        if run is None:
            return
        run["status"] = "completed"

    def mark_run_failed(self, run_id: str, error: str):
        run = self.runs.get(run_id)
        if run is None:
            return
        run["status"] = "failed"
        run["error"] = error
