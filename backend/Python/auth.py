from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from dotenv import load_dotenv

import os

# módulos
import models
import schemas
import database

# Carga las variables de entorno del archivo .env
load_dotenv()

# --- CONFIGURACIÓN DE SEGURIDAD ---
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# 1. Contexto para el hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 2. Esquema de seguridad de FastAPI (URL para obtener el token es '/api/py/token')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/py/token")


# --- FUNCIONES AUXILIARES DE AUTENTICACIÓN ---
# Función para verificar contraseña en texto plano coincide con su hash
def verify_password(plain_password, password):
    return pwd_context.verify(plain_password, password)

# Función para crear el hash de una contraseña nueva
def get_password_hash(password):
    return pwd_context.hash(password)

# Función para crear un nuevo token de acceso JWT
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



# --- FUNCIÓN DE DEPENDENCIA PARA PROTEGER RUTAS ---
# Función para obtener un usuario de la BD por su email
def get_user(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# Esta es la dependencia principal de seguridad.
# validar el token y devolver el usuario autenticado.
async def get_current_user(request: Request, token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    # Define la excepción que se lanzará si el token no es válido
    # --- LÍNEAS PARA DEPURAR ---
    #print("--- DEBUGGING AUTH ---")
    #print("Cabeceras recibidas:", request.headers)
    #print("Token extraído por FastAPI:", token)

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Intenta decodificar el token JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub") # 'sub' (subject) es nuestro email
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
    # Busca al usuario en la base de datos
    user = get_user(db, email=token_data.email)
    if user is None:
        raise credentials_exception
        
    # Si todo ok, devuelve el objeto del usuario
    return user