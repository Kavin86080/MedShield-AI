from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from backend.api.dependencies import get_current_doctor, get_db
from backend.models.doctor import Doctor
from backend.schemas.ai_conversation import ChatRequest, ChatResponse
from backend.services.rag_service import rag_service
from backend.services.consultation_service import consultation_service

router = APIRouter(prefix="/api/consultations", tags=["Chat"])

@router.post("/{id}/chat", response_model=ChatResponse)
def ask_ai_assistant(
    id: int,
    request: Request,
    payload: ChatRequest,
    current_doctor: Doctor = Depends(get_current_doctor),
    db: Session = Depends(get_db)
):
    """Submit a question to the clinical QA assistant for this consultation."""
    # Verify consultation exists and belongs to doctor
    consultation = consultation_service.get_consultation(db, consultation_id=id, doctor_id=current_doctor.id)
    if not consultation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consultation not found or unauthorized access."
        )
        
    client_ip = request.client.host if request.client else None
    
    try:
        # Run chat query
        chat_msg = rag_service.ask_rag(
            db,
            consultation_id=id,
            question=payload.question,
            doctor_id=current_doctor.id,
            ip_address=client_ip
        )
        return chat_msg
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error running QA request: {str(e)}"
        )

@router.get("/{id}/chat-history", response_model=List[ChatResponse])
def get_consultation_chat_history(
    id: int,
    current_doctor: Doctor = Depends(get_current_doctor),
    db: Session = Depends(get_db)
):
    """Retrieve full chronological conversation history for this consultation session."""
    # Verify consultation exists and belongs to doctor
    consultation = consultation_service.get_consultation(db, consultation_id=id, doctor_id=current_doctor.id)
    if not consultation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consultation not found or unauthorized access."
        )
        
    return rag_service.get_conversation_history(db, consultation_id=id)
