from fastapi import FastAPI, Depends
from fastapi import WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session, sessionmaker
import asyncio

from .config import engine

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_session(): #creates a new session whenever invoked. so a new session for every query
    with SessionLocal() as session:
        yield session

cache_q = None
def set_queue(q):
    global cache_q
    cache_q = q

app = FastAPI()

#cors middleware to allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:5173"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

@app.get('/')
def root():
    # session: Session=Depends(get_session) is syntax for dependency injection in fastapi. Session is type hint here
    return {"this is from root endpoint"}

@app.websocket('/ws_test')
async def send_data(websocket: WebSocket, session: Session = Depends(get_session)):
    await websocket.accept()
     
    try:
        while True:
            rear = cache_q.peek()
            if rear:
                data = cache_q.rear.data
            
            await websocket.send_json(data)
        
            await asyncio.sleep(1)
    except (WebSocketDisconnect):
        print('Websocket connection closed!')
