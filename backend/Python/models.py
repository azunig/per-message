# models.py
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, Enum, TIMESTAMP
from sqlalchemy.orm import relationship # <-- CAMBIO 1: Importamos 'relationship'
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    
    # Añadimos las marcas de tiempo, ya que son datos útiles para devolver en la API.
    # SQLAlchemy no intentará escribirlas si la base de datos las gestiona por defecto.
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')

    # La relación con los mensajes
    messages = relationship("Message", back_populates="owner")


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True) 
    parent_id = Column(Integer, ForeignKey("messages.id"), nullable=True)
    process_id = Column(Integer, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    type = Column(Enum('comentario', 'solicitud', 'pregunta', 'email', 'respuesta'), nullable=False)
    message = Column(Text, nullable=False)
    attachment_url = Column(String(2048), nullable=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    
    # Relación: Un mensaje pertenece a un usuario (owner)
    owner = relationship("User", back_populates="messages")