# Simple tool registry and helper functions for the code-review workflow
from typing import Dict, Any, Callable
import re

def extract_functions_tool(state: Dict[str, Any], tools):
    code = state.get("code", "")
    # very naive function extractor: count 'def ' occurrences and extract function names
    funcs = re.findall(r"def\s+(\w+)\s*\(", code)
    state_updates = {"functions": funcs, "function_count": len(funcs)}
    return {"state_updates": state_updates, "next": "check_complexity"}

def check_complexity_tool(state: Dict[str, Any], tools):
    # heuristic: longer function name + longer body -> higher score (fake metric)
    code = state.get("code", "")
    func_count = state.get("function_count", 0)
    # naive complexity: number of lines divided by functions (or lines if 0)
    lines = code.count("\n") + 1
    complexity = lines // max(1, func_count)
    state_updates = {"complexity": complexity}
    # branching example
    if complexity > 50:
        # if very complex, detect issues first
        return {"state_updates": state_updates, "next": "detect_issues"}
    return {"state_updates": state_updates, "next": "detect_issues"}

def detect_issues_tool(state: Dict[str, Any], tools):
    code = state.get("code", "")
    issues = []
    if "TODO" in code:
        issues.append("has_todo")
    if "print(" in code:
        issues.append("debug_prints")
    # simplistic rule: long lines
    long_lines = [i+1 for i,l in enumerate(code.splitlines()) if len(l) > 120]
    if long_lines:
        issues.append(f"long_lines:{long_lines[:3]}")
    state_updates = {"issues": issues, "issue_count": len(issues)}
    return {"state_updates": state_updates, "next": "suggest_improvements"}

def suggest_improvements_tool(state: Dict[str, Any], tools):
    suggestions = []
    if state.get("issue_count",0) > 0:
        suggestions.append("remove debug prints / address TODOs")
    if state.get("complexity",0) > 30:
        suggestions.append("refactor large functions into smaller units")
    # quality score heuristic
    quality_score = max(0, 100 - (state.get("complexity",0) + state.get("issue_count",0)*10))
    state_updates = {"suggestions": suggestions, "quality_score": quality_score}
    # loop check: continue improvements until quality_score >= threshold
    threshold = state.get("threshold", 80)
    if quality_score < threshold:
        # set directive to loop back to 'suggest_improvements' after making a simulated change
        # simulate a change by increasing quality
        state_updates["quality_score"] = quality_score + 30
        state_updates["_goto"] = "suggest_improvements" if state_updates["quality_score"] < threshold else None
    return {"state_updates": state_updates, "next": None}

tool_registry = {
    "extract_functions": extract_functions_tool,
    "check_complexity": check_complexity_tool,
    "detect_issues": detect_issues_tool,
    "suggest_improvements": suggest_improvements_tool
}
