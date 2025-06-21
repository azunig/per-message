# crud.py (versión final y correcta)
from sqlalchemy.orm import Session
import models, schemas

def get_messages_by_process(db: Session, process_id: int):
    return db.query(models.Message).filter(models.Message.process_id == process_id).order_by(models.Message.created_at.asc()).all()

def create_message(db: Session, message: schemas.MessageCreate, user_id: int):
    # La forma correcta es añadir el user_id al diccionario de datos
    message_data = message.model_dump()
    db_message = models.Message(
        **message_data, 
        user_id=user_id
    )
    db.add(db_message)
    db.flush() 
    db.refresh(db_message)
    db.commit()
    return db_message.id


def get_messages_for_user(db: Session, user_id: int):
    """
    Obtiene todos los mensajes creados por un usuario específico.
    """
    return db.query(models.Message).filter(models.Message.user_id == user_id).order_by(models.Message.created_at.desc()).all()


def get_message(db: Session, message_id: int):
    """
    Obtiene un único mensaje por su ID.
    """
    return db.query(models.Message).filter(models.Message.id == message_id).first()