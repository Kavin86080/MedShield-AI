# Import all database models so they are registered on the metadata Base.
# This file is used by Alembic migrations.

from backend.database.database import Base
from backend.models.doctor import Doctor
from backend.models.consultation import Consultation
from backend.models.uploaded_document import UploadedDocument
from backend.models.ai_conversation import AIConversation
from backend.models.generated_report import GeneratedReport
from backend.models.audit_log import AuditLog
