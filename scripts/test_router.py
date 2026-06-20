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

from agents.agent_router import (
    AgentRouter
)

router = AgentRouter()

questions = [
    "What disease causes fever?",
    "Analyze chest X-ray image",
    "Generate patient report",
    "What is MediSense?",
    "Summarize this research paper"
]

for q in questions:

    state = AgentState(
        question=q
    )

    state = router.run(
        state
    )

    print(
        f"{q} -> {state.metadata['route']}"
    )