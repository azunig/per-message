from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
import collections

import crud, models, schemas, auth
from database import Base, engine, get_db 

# La línea create_all se movió aquí para asegurar que todo se importa antes.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Python Messaging API")

# --- ENDPOINTS DE AUTENTICACIÓN ---

@app.post("/api/py/users/", response_model=schemas.User, status_code=201, tags=["Authentication"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)): # <-- Esto ahora funciona
    db_user = auth.get_user(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = auth.get_password_hash(user.password)
    new_user = models.User(email=user.email, name=user.name, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/api/py/token", response_model=schemas.Token, tags=["Authentication"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)): # <-- Esto ahora funciona
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
    db: Session = Depends(get_db), # <-- Esto ahora funciona
    current_user: models.User = Depends(auth.get_current_user)
):
    return crud.create_message(db=db, message=message, user_id=current_user.id)


@app.get("/api/py/processes/{process_id}/thread/", response_model=List[schemas.Message], tags=["Messages"])
def read_message_thread(
    process_id: int, 
    db: Session = Depends(get_db), # <-- Esto ahora funciona
    current_user: models.User = Depends(auth.get_current_user)
):
    db_messages = crud.get_messages_by_process(db, process_id=process_id)
    if not db_messages:
        return []

    message_map = collections.defaultdict(list)