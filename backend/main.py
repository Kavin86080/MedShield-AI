from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import shutil
from pathlib import Path

# Database auto-init
from backend.database.init_db import init_db

# UI router — always available regardless of AI module availability
from backend.api.ui_routes import router as ui_router

# New enterprise backend routers — always available
from backend.api.auth import router as auth_router
from backend.api.doctor_routes import router as doctor_router
from backend.api.consultation_routes import router as consultation_router
from backend.api.upload_routes import router as upload_router
from backend.api.chat_routes import router as chat_router
from backend.api.report_routes import router as report_router

# Legacy AI routers — wrapped in try/except to handle environments
# where TensorFlow DLL fails to load (CPU lacks AVX/AVX2 instructions)
_legacy_routers_available = False
try:
    from backend.api.medical_routes import router as medical_router
    from backend.api.document_routes import router as document_router
    from backend.api.image_routes import router as image_router
    from backend.api.orchestrator_routes import router as orchestrator_router
    _legacy_routers_available = True
    print("Legacy AI routers loaded successfully.")
except Exception as _legacy_import_err:
    print(f"Warning: Legacy AI routers could not be loaded ({type(_legacy_import_err).__name__}: {_legacy_import_err}). "
          "Enterprise API endpoints remain fully operational.")

# Initialize database tables on startup
try:
    init_db()
    print("Database tables initialized successfully.")
except Exception as e:
    print(f"Warning: Database initialization failed: {e}")

app = FastAPI(
    title="MedShield-X API",
    version="1.0"
)

# CORS middleware to allow frontend connection during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In enterprise production, specify the client origin domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure standard directories exist
UPLOAD_DIR = Path("frontend/static/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
Path("outputs").mkdir(parents=True, exist_ok=True)

# Mount static web assets and outputs directory
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")

# Mount React build assets directory if it exists
DIST_ASSETS_DIR = Path("frontend/dist/assets")
if DIST_ASSETS_DIR.exists():
    app.mount("/assets", StaticFiles(directory=str(DIST_ASSETS_DIR)), name="assets")

@app.post("/upload")
def upload_file(file: UploadFile = File(...)):
    """Legacy file upload endpoint."""
    try:
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return {
            "filename": file.filename,
            "url": f"/static/uploads/{file.filename}",
            "local_path": str(file_path.resolve())
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ── UI Router (always included — serves all Jinja2 pages) ────────────────────
app.include_router(ui_router)

# ── Enterprise API Routers (always included) ──────────────────────────────────
app.include_router(auth_router)
app.include_router(doctor_router)
app.include_router(consultation_router)
app.include_router(upload_router)
app.include_router(chat_router)
app.include_router(report_router)

# ── Legacy AI Routers (only if AI modules loaded successfully) ────────────────
if _legacy_routers_available:
    app.include_router(medical_router)
    app.include_router(document_router)
    app.include_router(image_router)
    app.include_router(orchestrator_router)

# NOTE: The catch-all SPA route has been intentionally removed.
# The Jinja2 ui_router (ui_routes.py) handles all page rendering.
# Keeping the React dist catch-all here would override all template routes.