# models.py
from sqlalchemy import Boolean, Column, ForeignKey, BigInteger, String, Text, Enum, TIMESTAMP
# Importación directa
from database import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(BigInteger, primary_key=True, index=True)
    parent_id = Column(BigInteger, ForeignKey("messages.id"), nullable=True)
    process_id = Column(BigInteger, nullable=False, index=True)
    type = Column(Enum('comentario', 'solicitud', 'pregunta', 'email'), nullable=False, name="message_type_enum")
    message = Column(Text, nullable=False)
    attachment_url = Column(String(2048), nullable=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')