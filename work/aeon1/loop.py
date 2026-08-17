"""AEON 1.0 workflow with durable LangGraph checkpoints and evidence."""
from __future__ import annotations

import json
from pathlib import Path
from typing import TypedDict

from autocorrect import evaluate_correction, propose_correction
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph
from memory_store import remember

ROOT = Path(__file__).parent
STATE = ROOT / "aeon_state.json"
CHECKPOINTS = ROOT / "aeon_checkpoints.sqlite"


class AeonState(TypedDict, total=False):
    version: str
    goal: str
    status: str
    errors: list[str]
    evidence: list[str]
    next_action: str


def load_state() -> dict:
    return json.loads(STATE.read_text(encoding="utf-8"))


def validate_node(state: AeonState) -> AeonState:
    source = load_state()
    errors = []
    if source.get("version") != "1.0.0":
        errors.append("version-mismatch")
    for field in ("active_goal", "next_action", "principles"):
        if field not in source:
            errors.append(f"missing:{field}")
    return {
        "version": source.get("version", ""),
        "goal": source.get("active_goal", ""),
        "status": "validated" if not errors else "needs-repair",
        "errors": errors,
        "evidence": ["state-file-readable", "required-fields-present", "langgraph-node-executed"] if not errors else [],
        "next_action": source.get("next_action", "Define next action"),
    }


def persist_node(state: AeonState) -> AeonState:
    source = load_state()
    source["status"] = state["status"]
    source["last_validation"] = {
        "ok": state["status"] == "validated",
        "errors": state.get("errors", []),
        "evidence": state.get("evidence", []),
    }
    correction = evaluate_correction(propose_correction(state.get("errors", [])))
    source["last_validation"]["correction"] = correction
    remember("validation", state["status"], state.get("evidence", []))
    STATE.write_text(json.dumps(source, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return state


def build_graph():
    graph = StateGraph(AeonState)
    graph.add_node("validate", validate_node)
    graph.add_node("persist", persist_node)
    graph.add_edge(START, "validate")
    graph.add_edge("validate", "persist")
    graph.add_edge("persist", END)
    return graph


def run_once(thread_id: str = "aeon-main") -> dict:
    with SqliteSaver.from_conn_string(str(CHECKPOINTS)) as checkpointer:
        app = build_graph().compile(checkpointer=checkpointer)
        return app.invoke({}, {"configurable": {"thread_id": thread_id}})


if __name__ == "__main__":
    print(json.dumps(run_once(), indent=2, ensure_ascii=False))
