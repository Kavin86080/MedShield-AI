from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

# Initialize template search paths for both templates and components
templates = Jinja2Templates(directory=["frontend/templates", "frontend/components"])

@router.get("/", response_class=HTMLResponse)
def get_dashboard_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request, "active_page": "dashboard"})

@router.get("/assistant", response_class=HTMLResponse)
def get_assistant_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request, "active_page": "assistant"})

@router.get("/orchestrator-page", response_class=HTMLResponse)
def get_orchestrator_page(request: Request):
    return templates.TemplateResponse("orchestrator.html", {"request": request, "active_page": "orchestrator"})

@router.get("/xray", response_class=HTMLResponse)
def get_xray_page(request: Request):
    return templates.TemplateResponse("xray.html", {"request": request, "active_page": "xray"})

@router.get("/document", response_class=HTMLResponse)
def get_document_page(request: Request):
    return templates.TemplateResponse("document.html", {"request": request, "active_page": "document"})

@router.get("/passport", response_class=HTMLResponse)
def get_passport_page(request: Request):
    return templates.TemplateResponse("passport.html", {"request": request, "active_page": "passport"})

@router.get("/reports", response_class=HTMLResponse)
def get_reports_page(request: Request):
    return templates.TemplateResponse("reports.html", {"request": request, "active_page": "reports"})

@router.get("/explainability", response_class=HTMLResponse)
def get_explainability_page(request: Request):
    return templates.TemplateResponse("explainability.html", {"request": request, "active_page": "explainability"})

@router.get("/robustness", response_class=HTMLResponse)
def get_robustness_page(request: Request):
    return templates.TemplateResponse("robustness.html", {"request": request, "active_page": "robustness"})

@router.get("/research", response_class=HTMLResponse)
def get_research_page(request: Request):
    return templates.TemplateResponse("research.html", {"request": request, "active_page": "research"})

@router.get("/settings", response_class=HTMLResponse)
def get_settings_page(request: Request):
    return templates.TemplateResponse("settings.html", {"request": request, "active_page": "settings"})

@router.get("/upload", response_class=HTMLResponse)
def get_upload_page(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request, "active_page": "upload"})

@router.get("/evidence-explorer", response_class=HTMLResponse)
def get_evidence_explorer_page(request: Request):
    return templates.TemplateResponse("evidence_explorer.html", {"request": request, "active_page": "evidence_explorer"})

@router.get("/consultations", response_class=HTMLResponse)
def get_consultations_page(request: Request):
    return templates.TemplateResponse("consultations.html", {"request": request, "active_page": "consultations"})

@router.get("/profile", response_class=HTMLResponse)
def get_profile_page(request: Request):
    return templates.TemplateResponse("profile.html", {"request": request, "active_page": "profile"})

@router.get("/login", response_class=HTMLResponse)
def get_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "active_page": "login"})

@router.get("/register", response_class=HTMLResponse)
def get_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request, "active_page": "register"})
