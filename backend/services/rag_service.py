from typing import Dict, List, Optional
from sqlalchemy.orm import Session

from backend.rag.pipeline.dynamic_rag_pipeline import DynamicRAGPipeline
from backend.repositories.uploaded_document_repository import UploadedDocumentRepository
from backend.repositories.ai_conversation_repository import AIConversationRepository
from backend.models.uploaded_document import UploadedDocument
from backend.models.ai_conversation import AIConversation
from backend.services.audit_service import audit_service

class RAGService:
    def __init__(self):
        self.doc_repo = UploadedDocumentRepository()
        self.chat_repo = AIConversationRepository()
        # In-memory dictionary caching active RAG pipelines for consultations
        self._sessions: Dict[int, DynamicRAGPipeline] = {}

    def get_pipeline(self, db: Session, consultation_id: int) -> DynamicRAGPipeline:
        """Retrieve the cached RAG pipeline session or rebuild it from stored files."""
        if consultation_id not in self._sessions:
            pipeline = DynamicRAGPipeline()
            # Fetch and reload all previously ingested documents for this consultation
            docs = self.doc_repo.get_by_consultation(db, consultation_id)
            for doc in docs:
                try:
                    pipeline.upload_document(doc.file_path)
                except Exception as e:
                    # Log document reload failures, but don't crash session loading
                    print(f"Failed to reload document {doc.filename} into RAG session: {e}")
            
            # Reconstruct memory history if conversations exist
            chats = self.chat_repo.get_by_consultation(db, consultation_id)
            for chat in chats:
                pipeline.memory.add_message("doctor", chat.question)
                pipeline.memory.add_message("assistant", chat.answer)
                
            self._sessions[consultation_id] = pipeline
        return self._sessions[consultation_id]

    def remove_session(self, consultation_id: int):
        """Evict a consultation pipeline session from cache."""
        if consultation_id in self._sessions:
            self._sessions.pop(consultation_id)

    def upload_document(
        self, 
        db: Session, 
        consultation_id: int, 
        filename: str, 
        file_path: str, 
        file_type: str, 
        doctor_id: int, 
        ip_address: Optional[str] = None
    ) -> UploadedDocument:
        """Persist document upload metadata and ingest it into the RAG Pipeline."""
        new_doc = UploadedDocument(
            consultation_id=consultation_id,
            filename=filename,
            file_path=file_path,
            file_type=file_type
        )
        created_doc = self.doc_repo.create(db, new_doc)
        
        # Load and ingest in pipeline
        pipeline = self.get_pipeline(db, consultation_id)
        pipeline.upload_document(file_path)
        
        # Log audit log
        audit_service.log_action(db, doctor_id, f"upload_document: {created_doc.id} for consultation {consultation_id}", ip_address)
        return created_doc

    def ask_rag(
        self, 
        db: Session, 
        consultation_id: int, 
        question: str, 
        doctor_id: int, 
        ip_address: Optional[str] = None
    ) -> AIConversation:
        """Send a clinical inquiry to the consultation RAG pipeline, persist Q&A, and return database object."""
        pipeline = self.get_pipeline(db, consultation_id)
        result = pipeline.ask(question)
        
        response_data = result.get("response", {})
        answer = response_data.get("answer", "No response generated.")
        confidence = response_data.get("confidence", 0.0)
        evidence = response_data.get("evidence", [])
        citations = response_data.get("citations", [])
        
        new_chat = AIConversation(
            consultation_id=consultation_id,
            question=question,
            answer=answer,
            confidence_score=confidence,
            evidence=evidence,
            citations=citations
        )
        created_chat = self.chat_repo.create(db, new_chat)
        
        # Log action
        audit_service.log_action(db, doctor_id, f"ask_rag_query: {created_chat.id} for consultation {consultation_id}", ip_address)
        return created_chat

    def get_conversation_history(self, db: Session, consultation_id: int) -> List[AIConversation]:
        """Retrieve the Q&A list for a consultation."""
        return self.chat_repo.get_by_consultation(db, consultation_id)

    def get_uploaded_documents(self, db: Session, consultation_id: int) -> List[UploadedDocument]:
        """Retrieve list of files uploaded for a consultation."""
        return self.doc_repo.get_by_consultation(db, consultation_id)

# Instantiate global service singleton
rag_service = RAGService()
