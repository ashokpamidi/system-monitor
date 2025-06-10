from typing import Optional
from fastapi import FastAPI, Depends, Query
from fastapi import WebSocket, WebSocketDisconnect
from websockets.exceptions import ConnectionClosed
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, DateTime, desc
from sqlalchemy.orm import declarative_base,Session, sessionmaker
from pydantic import BaseModel
from typing import Optional
import asyncio
import websocket
import time

db_full_path = r"..\data\systemMonitoring.db"
sqlite_url = f'sqlite:///{db_full_path}'
connect_args = {'check_same_thread': False} #this allows api to use the same db in different threads which is useful if one single request is using multiple threads

engine = create_engine(sqlite_url, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class appinfo(Base):
    __tablename__ = 'app_data'
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(String, nullable=False)
    total_active_processes = Column(Integer, nullable=False)
    app_name = Column(String, nullable=False)
    cursor_position = Column(String, nullable=False)

class ResponseTotalActiveProcesses(BaseModel):
    total_active_processes: Optional[int] = None #optional is a type hint that tells the value can be int or None

def get_session(): #creates a new session whenever invoked. so a new session for every query
    with SessionLocal() as session:
        yield session

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
            res = session.query(appinfo).order_by(desc(appinfo.id)).limit(1).first()
            # current_time = time.strftime('%H-%M-%S')
            data = {'id': res.id,'timestamp': res.timestamp,'total_active_processes': res.total_active_processes,'app_name': res.app_name,'cursor_position': res.cursor_position}
            await websocket.send_json(data)
        
            await asyncio.sleep(1)
    except (WebSocketDisconnect, ConnectionClosed):
        print('Websocket connection closed!')
    
@app.get('/test')
def send_items():
    return 221