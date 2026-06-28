from typing import List
from sqlalchemy.orm import Session
from backend.repositories.base_repository import BaseRepository
from backend.models.ai_conversation import AIConversation

class AIConversationRepository(BaseRepository[AIConversation]):
    def __init__(self):
        super().__init__(AIConversation)

    def get_by_consultation(self, db: Session, consultation_id: int) -> List[AIConversation]:
        """Fetch full conversation history for a specific consultation session in chronological order."""
        return db.query(AIConversation).filter(AIConversation.consultation_id == consultation_id).order_by(AIConversation.created_at.ascii if hasattr(AIConversation.created_at, "ascii") else AIConversation.created_at.asc()).all()
