# schemas.py

from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Optional

# ===================================================================
# --- Esquemas para el Usuario ---
# ===================================================================

# Esquema base con la información pública de un usuario
class UserBase(BaseModel):
    email: str
    name: Optional[str] = None

# Esquema para crear un nuevo usuario (recibe la contraseña)
class UserCreate(UserBase):
    password: str

# Esquema para devolver un usuario desde la API (SIN la contraseña)
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
    pass # No necesita campos adicionales

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