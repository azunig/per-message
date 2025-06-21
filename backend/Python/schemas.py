from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Optional

# ===================================================================
# --- Esquemas para el Usuario ---
# ===================================================================

# Esquema base usuario
class UserBase(BaseModel):
    email: str
    name: Optional[str] = None

# Esquema crea un nuevo usuario (contraseña)
class UserCreate(UserBase):
    password: str

# Esquema devolver un usuario API (SIN contraseña)
class User(UserBase):
    id: int
    
    # Configuración para que Pydantic pueda leer desde un modelo de SQLAlchemy
    model_config = ConfigDict(from_attributes=True)


# ===================================================================
# --- Esquemas para los Mensajes (Actualizados) ---
# ===================================================================

class MessageBase(BaseModel):
    message: str
    process_id: int
    parent_id: Optional[int] = None
    type: str = 'comentario'
    attachment_url: Optional[str] = None


class MessageCreate(MessageBase):
    message: str
    process_id: int


class Message(MessageBase):
    id: int
    created_at: datetime
    is_deleted: bool
    
    # CAMBIO IMPORTANTE: Ahora incluimos la información del dueño del mensaje
    user_id: int
    owner: User # <-- Anidamos el esquema 'User' para devolver sus datos
    
    # La relación recursiva para los hijos se mantiene
    children: List['Message'] = []

    model_config = ConfigDict(from_attributes=True)


class ReplyCreate(BaseModel):
    message: str
    type: str = 'comentario'
    attachment_url: Optional[str] = None


# ===================================================================
# --- Esquemas para la Autenticación (JWT) ---
# ===================================================================

# Esquema para la respuesta del endpoint de login
class Token(BaseModel):
    access_token: str
    token_type: str

# Esquema para los datos que guardamos dentro del propio token JWT
class TokenData(BaseModel):
    email: Optional[str] = None