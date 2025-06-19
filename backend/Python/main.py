# main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
import collections

# Importamos todos nuestros módulos
import crud, models, schemas, auth
from database import SessionLocal, Base, engine

# Esto creará las tablas 'users' y 'messages' si no existen
# cuando la aplicación se inicie por primera vez.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Python Messaging API")

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- ENDPOINTS DE AUTENTICACIÓN ---

@app.post("/api/py/users/", response_model=schemas.User, tags=["Authentication"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Endpoint para registrar un nuevo usuario.
    """
    db_user = auth.get_user(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = auth.get_password_hash(user.password)
    new_user = models.User(email=user.email, name=user.name, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/api/py/token", response_model=schemas.Token, tags=["Authentication"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Endpoint para iniciar sesión y obtener un token JWT.
    Espera datos de formulario con 'username' (que será nuestro email) y 'password'.
    """
    user = auth.get_user(db, email=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# --- ENDPOINTS DE MENSAJES (AHORA PROTEGIDOS) ---

@app.post("/api/py/messages/", response_model=schemas.Message, status_code=201, tags=["Messages"])
def create_new_message(
    message: schemas.MessageCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(auth.get_current_user) # <-- Dependencia de seguridad
):
    """
    Crea un nuevo mensaje. Solo para usuarios autenticados.
    """
    # Asociamos el mensaje con el usuario autenticado que nos da la dependencia
    return crud.create_message(db=db, message=message, user_id=current_user.id)

@app.get("/api/py/processes/{process_id}/thread/", response_model=List[schemas.Message], tags=["Messages"])
def read_message_thread(
    process_id: int, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(auth.get_current_user) # <-- Dependencia de seguridad
):
    """
    Obtiene un hilo de conversación. Solo para usuarios autenticados.
    """
    db_messages = crud.get_messages_by_process(db, process_id=process_id)
    if not db_messages:
        return []

    # La lógica para construir el árbol de mensajes no cambia
    message_map = collections.defaultdict(list)
    for msg in db_messages:
        message_map[msg.parent_id].append(msg)

    def build_tree(parent_id=None):
        node_children = []
        for child_msg in message_map[parent_id]:
            pydantic_msg = schemas.Message.model_validate(child_msg)
            pydantic_msg.children = build_tree(child_msg.id)
            node_children.append(pydantic_msg)
        return node_children

    return build_tree()