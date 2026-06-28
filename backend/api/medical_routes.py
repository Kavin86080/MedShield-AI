from fastapi import APIRouter

from agents.agent_state import (
    AgentState
)

from agents.orchestrator import (
    AgentOrchestrator
)

router = APIRouter()

orchestrator = (
    AgentOrchestrator()
)


@router.post(
    "/ask"
)
def ask_medical_question(
    payload: dict
):

    state = AgentState(
        question=
        payload["question"]
    )

    result = (
        orchestrator.run(
            state
        )
    )

    return result