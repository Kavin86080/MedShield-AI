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

from dotenv import load_dotenv

load_dotenv()

from agents.orchestrator import (
    AgentOrchestrator
)

agent = AgentOrchestrator()

report = agent.run(
    "What disease causes fever?"
)

print("\nFINAL REPORT")
print("=" * 60)

print(report)