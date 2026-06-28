from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from backend.api.dependencies import get_current_doctor, get_db
from backend.models.doctor import Doctor
from backend.schemas.generated_report import ReportGenerateRequest, GeneratedReportResponse
from backend.services.rag_service import rag_service
from backend.services.consultation_service import consultation_service
from backend.repositories.generated_report_repository import GeneratedReportRepository
from backend.models.generated_report import GeneratedReport
from backend.services.audit_service import audit_service

router = APIRouter(tags=["Reports"])
report_repo = GeneratedReportRepository()

@router.post("/generate-report")
def generate_report(payload: dict):
    """Legacy report generation endpoint preserved for compatibility."""
    patient_name = payload["patient_name"]
    age = payload["age"]
    gender = payload["gender"]
    xray_result = payload["xray_result"]
    notes = payload["clinical_notes"]
    
    report = f"""
Patient: {patient_name}

Age: {age}

Gender: {gender}

X-Ray Result: {xray_result}

Clinical Notes:
{notes}
"""
    return {
        "report": report
    }

@router.post("/api/consultations/{id}/reports", response_model=GeneratedReportResponse)
def compile_consultation_report(
    id: int,
    request: Request,
    payload: ReportGenerateRequest,
    current_doctor: Doctor = Depends(get_current_doctor),
    db: Session = Depends(get_db)
):
    """Compile and save a structured clinical summary report for the consultation using the AI reasoner."""
    # Verify consultation exists and belongs to doctor
    consultation = consultation_service.get_consultation(db, consultation_id=id, doctor_id=current_doctor.id)
    if not consultation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consultation not found or unauthorized access."
        )
        
    try:
        # Load the RAG pipeline session
        pipeline = rag_service.get_pipeline(db, consultation_id=id)
        
        # Craft a summarizing clinical report prompt
        prompt = (
            "Generate a highly detailed, professional, structured clinical summary report for this patient's consultation. "
            "Integrate findings from all uploaded clinical files, highlight abnormal indicators (e.g., blood test levels, imaging anomalies), "
            "summarize the queries and clinical observations made, cite the evidence, and outline clinical recommendations. "
            "The report must use formal medical language and be clearly structured with headings."
        )
        
        # Ask RAG pipeline
        result = pipeline.ask(prompt)
        content = result.get("response", {}).get("answer", "Failed to compile report summary.")
        
        # Save to database
        new_report = GeneratedReport(
            consultation_id=id,
            content=content,
            report_type=payload.report_type
        )
        created_report = report_repo.create(db, new_report)
        
        # Log action
        client_ip = request.client.host if request.client else None
        audit_service.log_action(
            db, 
            doctor_id=current_doctor.id, 
            action=f"generate_report: {created_report.id} for consultation {id}", 
            ip_address=client_ip
        )
        
        return created_report
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate clinical report: {str(e)}"
        )

@router.get("/api/consultations/{id}/reports", response_model=List[GeneratedReportResponse])
def get_consultation_reports(
    id: int,
    current_doctor: Doctor = Depends(get_current_doctor),
    db: Session = Depends(get_db)
):
    """Retrieve all reports generated for this consultation."""
    # Verify consultation exists and belongs to doctor
    consultation = consultation_service.get_consultation(db, consultation_id=id, doctor_id=current_doctor.id)
    if not consultation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consultation not found or unauthorized access."
        )
        
    return report_repo.get_by_consultation(db, consultation_id=id)