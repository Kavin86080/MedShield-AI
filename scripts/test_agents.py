import sys

from pathlib import Path

PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parent.parent
)

sys.path.insert(
    0,
    str(PROJECT_ROOT)
)

from agents.orchestrator import (
    AgentOrchestrator
)

from agents.agent_state import (
    AgentState
)

agent = (
    AgentOrchestrator()
)

state = AgentState(
    question=
    "What disease causes fever?"
)

report = (
    agent.run(
        state
    )
)

print(
    "\nFINAL REPORT"
)

print("=" * 60)

print(report)