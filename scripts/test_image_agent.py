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

from agents.image_agent import (
    ImageAgent
)

agent = (
    ImageAgent()
)

state = AgentState(
    question=
    "Analyze Chest X-Ray"
)

state.metadata[
    "image_path"
] = (
    "datasets/chest_xray/test/NORMAL/"
    + __import__("os").listdir(
        "datasets/chest_xray/test/NORMAL"
    )[0]
)

state = agent.run(
    state
)

print(
    "\nIMAGE AGENT REPORT"
)

print("=" * 60)

print(
    state.metadata[
        "prediction"
    ]
)

print()

print(
    state.answer
)