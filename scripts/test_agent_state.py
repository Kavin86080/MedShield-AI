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

from agents.agent_state import (
    AgentState
)

state = AgentState(
    question="What causes pneumonia?"
)

print("\nSTATE OBJECT")
print("=" * 50)

print(
    state.to_dict()
)