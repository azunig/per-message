from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

from typing import List
import collections

import crud, models, schemas, auth
from database import Base, engine, get_db 

# --- BLOQUE  CORS ---
origins = [
    "http://localhost:5173", # URL frontend Vue
]



# La línea create_all se movió aquí para asegurar que todo se importa antes.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Python Messaging API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Permite todos los métodos
    allow_headers=["*"], # Permite todas las cabeceras
)

# --- ENDPOINTS DE AUTENTICACIÓN ---

@app.post("/api/py/users/", response_model=schemas.User, status_code=201, tags=["Authentication"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)): # <-- Esto ahora funciona
    db_user = auth.get_user(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    #hashed_password = auth.get_password_hash(user.password)
    new_user = models.User(email=user.email, name=user.name, password=auth.get_password_hash(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/api/py/token", response_model=schemas.Token, tags=["Authentication"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)): # <-- Esto ahora funciona
    user = auth.get_user(db, email=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.password):
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
    db: Session = Depends(get_db), # <-- Esto ahora funciona, ni pico idea por qué antes no...
    current_user: models.User = Depends(auth.get_current_user)
):
    """
    Crea un nuevo mensaje parent.
    """

    print(f"➡️  Iniciando create_new_message (mensaje raíz)")
    print(f"    - Usuario autenticado: ID {current_user.id} ({current_user.email})")
    print(f"    - Datos recibidos: {message}")

    # 1. función CRUD y agarramos el ID
    print("    - Llamando a crud.create_message para guardar...")
    new_message_id = crud.create_message(db=db, message=message, user_id=current_user.id)
    print(f"    - ✅ Mensaje guardado en la BD. Nuevo ID: {new_message_id}")

    # 2. ID para obtener el objeto completo desde la BD
    print(f"    - Obteniendo el mensaje completo con ID {new_message_id} para la respuesta...")
    db_message = crud.get_message(db, message_id=new_message_id)
    print("    - ✅ Objeto fresco obtenido.")

    # 3. Devolvemos el objeto, que ahora con 'created_at'... problema del refresco y el flush.
    print("⬅️  Finalizando create_new_message y devolviendo la respuesta.")
    
    return db_message


@app.get("/api/py/processes/{process_id}/thread/", response_model=List[schemas.Message], tags=["Messages"])
def read_message_thread(
    process_id: int, 
    db: Session = Depends(get_db), # <-- Esto ahora funciona
    current_user: models.User = Depends(auth.get_current_user)
):
    db_messages = crud.get_messages_by_process(db, process_id=process_id)
    if not db_messages:
        return []

    # --- CORRECCIÓN  ---

    # 1. PRIMERO, mapa vacío.
    message_map = collections.defaultdict(list)

    # 2. SEGUNDO, datos del bucle.
    for msg in db_messages:
        message_map[msg.parent_id].append(msg)

    # build_tree puede usar el mapa ya poblado.
    def build_tree(parent_id=None):
        node_children = []
        #  todos los hijos para el parent_id actual en  mapa
        for child_msg in message_map.get(parent_id, []):
            # (SQLAlchemy) a esquema de respuesta (Pydantic)
            pydantic_msg = schemas.Message.model_validate(child_msg)
            # Recursivamente, los hijos de este hijo
            pydantic_msg.children = build_tree(child_msg.id)
            node_children.append(pydantic_msg)
        return node_children

    # 3. construcción del árbol desde la raíz (parent_id=None)
    return build_tree(None)

@app.get("/api/py/messages/", response_model=List[schemas.Message], tags=["Messages"])
def read_all_messages(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """
    Obtiene todos los hilos de mensajes para el usuario autenticado.
    """
    
    messages = crud.get_messages_for_user(db=db, user_id=current_user.id)
    return messages

# --- NUEVO ENDPOINT ---
@app.get("/api/py/messages/me", response_model=List[schemas.Message], tags=["Messages"])
def read_my_messages(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """
    Obtiene todos los mensajes del usuario actualmente autenticado.
    """
    # 1. La dependencia 'get_current_user' ya nos da el usuario del token.
    # 2. Usamos nuestra nueva función del CRUD.
    # 3. Le pasamos el ID del usuario que obtuvimos del token.
    messages = crud.get_messages_for_user(db=db, user_id=current_user.id)
    return messages


@app.post("/api/py/messages/{message_id}/reply", response_model=schemas.Message, status_code=201, tags=["Messages"])
def create_reply(
    message_id: int,
    reply: schemas.ReplyCreate, # <-- nuevo y simple esquema o.O
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """
    Crea una respuesta a un mensaje existente.
    """
    print(f"➡️  Iniciando create_reply para el mensaje padre ID: {message_id}")

    # 1. Busca el mensaje padre para asegura que existe!
    #print("    - Buscando mensaje padre en la BD...")
    parent_message = crud.get_message(db, message_id=message_id)
    if not parent_message:
        print(f"❌ ERROR: Mensaje padre con ID {message_id} no encontrado.")
        raise HTTPException(status_code=404, detail="Parent message not found")
    
    #print(f"    - ✅ Mensaje padre encontrado (ID: {parent_message.id}, Proceso ID: {parent_message.process_id})")

    # 2. Objeto de datos completo para la nueva respuesta.
    #    el process_id del padre para mantener la consistencia de la conversa.
    full_message_data = schemas.MessageCreate(
        message=reply.message,
        type=reply.type,
        attachment_url=reply.attachment_url,
        parent_id=parent_message.id, # El id del mensaje al que respondemos
        process_id=parent_message.process_id # Heredamos el process_id
    )
    #print(f"    - Datos de la nueva respuesta preparados: {full_message_data}")

    # 4. función CRUD existente para guardar en la base de datos.
    #print("    - Llamando a crud.create_message para guardar...")
    new_reply_id = crud.create_message(db=db, message=full_message_data, user_id=current_user.id)
    #print(f"    - ✅ Mensaje guardado en la BD. Nuevo ID: {new_reply_id}")


    # 5. ID para obtener el objeto completo y "nueo" de la respuesta
    #print(f"    - Obteniendo el mensaje completo con ID {new_reply_id} para la respuesta...")
    db_reply = crud.get_message(db, message_id=new_reply_id)
    #print("    - ✅ Objeto obtenido.")

    # 6. Devolvemos el objeto nueo.
    #print("Finalizando create_reply y devolviendo la respuesta.")
    return db_reply