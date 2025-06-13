# crud.py
from sqlalchemy.orm import Session
# Importaciones directas
import models, schemas

def get_messages_by_process(db: Session, process_id: int):
    return db.query(models.Message).filter(models.Message.process_id == process_id).order_by(models.Message.created_at.asc()).all()

def create_message(db: Session, message: schemas.MessageCreate):
    db_message = models.Message(**message.model_dump())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message