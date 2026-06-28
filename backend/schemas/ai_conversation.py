from datetime import datetime
from typing import List, Optional, Any
from pydantic import BaseModel

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    id: int
    consultation_id: int
    question: str
    answer: str
    confidence_score: Optional[float]
    evidence: Optional[List[Any]]
    citations: Optional[List[Any]]
    created_at: datetime

    class Config:
        from_attributes = True
