from typing import Generic, Type, TypeVar, List, Optional
from sqlalchemy.orm import Session
from backend.database.database import Base

ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: any) -> Optional[ModelType]:
        """Fetch a single record by ID."""
        return db.query(self.model).filter(self.model.id == id).first()

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Fetch all records with offset/limit paging."""
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: ModelType) -> ModelType:
        """Create and commit a new database record."""
        db.add(obj_in)
        db.commit()
        db.refresh(obj_in)
        return obj_in

    def update(self, db: Session, db_obj: ModelType, update_data: dict) -> ModelType:
        """Update fields of an existing record."""
        for field, value in update_data.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, id: any) -> bool:
        """Delete a record by ID."""
        obj = db.query(self.model).filter(self.model.id == id).first()
        if obj:
            db.delete(obj)
            db.commit()
            return True
        return False
