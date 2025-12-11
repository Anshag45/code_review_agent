import asyncio
from typing import Dict, Any, Callable, Optional
from app.tools.code_tools import tool_registry


class Node:
    def __init__(self, name: str, func: Callable, is_async: bool = False):
        self.name = name
        self.func = func
        self.is_async = is_async

    async def run(self, state: Dict[str, Any]):
        if asyncio.iscoroutinefunction(self.func):
            return await self.func(state, tool_registry)
        else:
            # run sync in threadpool
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(None, lambda: self.func(state, tool_registry))

class Graph:
    def __init__(self, nodes: Dict[str, Node], edges: Dict[str, Any], start: str):
        self.nodes = nodes
        self.edges = edges
        self.start = start

    @classmethod
    def from_dict(cls, d: Dict[str, Any]):
        nodes = {}
        for name, fn in d["nodes"].items():
            # fn is a python function object in our simple sample; for generic json you'd map names to functions
            nodes[name] = Node(name, fn)
        edges = d.get("edges", {})
        start = d.get("start")
        return cls(nodes, edges, start)

    async def execute(self, initial_state: Dict[str, Any], run_id: str, store):
        state = dict(initial_state)
        current = self.start
        store.append_run_log(run_id, f"starting run at node: {current}")
        try:
            visited = 0
            while current:
                node = self.nodes[current]
                store.append_run_log(run_id, f"running node: {current}")
                result = await node.run(state)
                # node can modify state in-place and/or return control instructions
                if isinstance(result, dict):
                    state.update(result.get("state_updates", {}))
                    next_node = result.get("next")
                else:
                    next_node = self.edges.get(current)
                visited += 1
                store.update_run_state(run_id, state)
                if visited > 1000:
                    raise RuntimeError("possible infinite loop")
                # branching: if state has _goto override
                if state.get("_goto"):
                    next_node = state.pop("_goto")
                # simple loop condition handled by a node setting next to itself or another
                current = next_node
                await asyncio.sleep(0)  # yield
            store.append_run_log(run_id, "completed")
            store.mark_run_completed(run_id)
        except Exception as e:
            store.append_run_log(run_id, f"failed: {e}")
            store.mark_run_failed(run_id, str(e))
