# crud.py (versión final y correcta)
from sqlalchemy.orm import Session
import models, schemas

def get_messages_by_process(db: Session, process_id: int):
    return db.query(models.Message).filter(models.Message.process_id == process_id).order_by(models.Message.created_at.asc()).all()

def create_message(db: Session, message: schemas.MessageCreate, user_id: int):
    # La forma correcta es añadir el user_id al diccionario de datos
    message_data = message.model_dump()
    db_message = models.Message(**message_data, user_id=user_id)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message