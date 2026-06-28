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
    "/analyze-document"
)
def analyze_document(
    payload: dict
):

    question = (
        payload.get(
            "question",
            ""
        )
    )

    pdf_path = (
        payload.get(
            "pdf_path"
        )
    )

    print("\n" + "=" * 60)
    print("DOCUMENT ANALYSIS REQUEST")
    print("=" * 60)

    print("\nQUESTION:")
    print(question)

    print("\nPDF PATH:")
    print(pdf_path)

    # Load uploaded PDF

    if pdf_path:

        if hasattr(
            orchestrator,
            "document_agent"
        ):

            print("\nLOADING DOCUMENT...")

            orchestrator.document_agent.load_document(
                pdf_path
            )

            print(
                "\nDOCUMENT LOADED SUCCESSFULLY"
            )

        else:

            return {
                "error":
                "Document Agent not initialized."
            }

    else:

        print(
            "\nWARNING: No PDF path received!"
        )

    state = AgentState(
        question=question
    )

    print(
        "\nRUNNING DOCUMENT AGENT..."
    )

    state = (
        orchestrator.document_agent.run(
            state
        )
    )

    print(
        "\nDOCUMENT AGENT COMPLETED"
    )

    report = {
        "question": question,
        "answer": state.answer,
        "contexts": state.contexts,
        "route": "document_analysis"
    }

    return report