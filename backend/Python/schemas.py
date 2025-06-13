from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Optional

# --- Esquema base con los campos comunes ---
class MessageBase(BaseModel):
    message: str
    process_id: int
    parent_id: Optional[int] = None
    type: str = 'comentario'
    attachment_url: Optional[str] = None

# --- Esquema para la creación de un mensaje (lo que recibe la API) ---
class MessageCreate(MessageBase):
    pass

# --- Esquema para la lectura (lo que devuelve la API) ---
# Este es un esquema recursivo: un mensaje puede contener una lista de mensajes (sus hijos)
class Message(MessageBase):
    id: int
    created_at: datetime
    is_deleted: bool
    children: List['Message'] = [] # Lista para las respuestas

    # Permite que Pydantic V2 trabaje con modelos de ORM
    model_config = ConfigDict(from_attributes=True)