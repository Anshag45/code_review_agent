# Build a sample graph object programmatically for the demo
from app.engine.graph import Graph, Node
from app.tools import code_tools


def build_code_review_graph():
    nodes = {
        "extract_functions": Node("extract_functions", code_tools.extract_functions_tool),
        "check_complexity": Node("check_complexity", code_tools.check_complexity_tool),
        "detect_issues": Node("detect_issues", code_tools.detect_issues_tool),
        "suggest_improvements": Node("suggest_improvements", code_tools.suggest_improvements_tool),
    }
    edges = {
        "extract_functions": "check_complexity",
        "check_complexity": "detect_issues",
        "detect_issues": "suggest_improvements",
        "suggest_improvements": None
    }
    start = "extract_functions"
    return Graph(nodes, edges, start)
