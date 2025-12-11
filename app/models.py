from pydantic import BaseModel
from typing import Dict, Any

class GraphSpec(BaseModel):
    nodes: Dict[str, Any]
    edges: Dict[str, Any]
    start: str
