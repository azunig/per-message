# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import collections

# Importaciones directas, ya no relativas
import crud, models, schemas
from database import SessionLocal, Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Python Messaging API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/py/messages/", response_model=schemas.Message, status_code=201)
def create_new_message(message: schemas.MessageCreate, db: Session = Depends(get_db)):
    return crud.create_message(db=db, message=message)

@app.get("/api/py/processes/{process_id}/thread/", response_model=List[schemas.Message])
def read_message_thread(process_id: int, db: Session = Depends(get_db)):
    db_messages = crud.get_messages_by_process(db, process_id=process_id)
    if not db_messages:
        raise HTTPException(status_code=404, detail="No messages found for this process")

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