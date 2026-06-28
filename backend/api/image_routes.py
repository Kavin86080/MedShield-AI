from fastapi import APIRouter

from agents.image_agent import ImageAgent
from agents.agent_state import AgentState

router = APIRouter()

image_agent = ImageAgent()

@router.post("/analyze-image")
def analyze_image(payload: dict):
    """Endpoint to analyze a chest X‑Ray image.

    Expects a JSON payload with an ``image_path`` key pointing to the
    uploaded image on the server. Returns a dictionary containing the
    prediction, optional Grad‑CAM heat‑map path, and a textual explanation.
    """
    # Initialise the agent state with a fixed question for provenance.
    state = AgentState(question="Analyze Chest X-Ray")

    # Attach the image path to the state metadata for the ImageAgent.
    state.metadata["image_path"] = payload.get("image_path")

    # Run the agent – it returns an updated state with results populated.
    state = image_agent.run(state)

    return {
        "prediction": state.metadata.get("prediction"),
        "heatmap_path": state.metadata.get("heatmap_path"),
        "explanation": state.answer,
    }