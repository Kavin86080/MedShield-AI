from fastapi import FastAPI

app = FastAPI(
    title="MedShield-X",
    description="Agentic Multimodal Healthcare AI Assistant",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "message": "MedShield-X is running successfully 🚀"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }