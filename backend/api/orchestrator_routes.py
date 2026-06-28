from fastapi import APIRouter

from agents.orchestrator import (
    AgentOrchestrator
)

from agents.agent_state import (
    AgentState
)

router = APIRouter()

orchestrator = (
    AgentOrchestrator()
)


@router.post(
    "/orchestrator"
)
def orchestrate(
    payload: dict
):

    state = AgentState(

        question=
        payload["question"]

    )

    # Optional inputs

    if "image_path" in payload:

        state.metadata[
            "image_path"
        ] = payload[
            "image_path"
        ]

    if "document_path" in payload:

        state.metadata[
            "document_path"
        ] = payload[
            "document_path"
        ]

    report = (
        orchestrator.run(
            state
        )
    )

    return report