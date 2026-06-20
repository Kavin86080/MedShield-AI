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

orchestrator = (
    AgentOrchestrator()
)

report = (
    orchestrator.run(
        "What is MediSense?"
    )
)

print("\nFINAL REPORT")
print("=" * 60)

print(report)