import asyncio
from datetime import datetime, timedelta
from typing import List, Dict
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy import inspect
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import delete
from sqlalchemy import String

QUEUE_LEN = 50
db_path = "../data/systemMonitoring.db"
table_name = 'app_data'
log = []

Base = declarative_base()
engine = create_engine(rf'sqlite:///{db_path}')

class appinfo(Base):
    __tablename__ = table_name
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(String, nullable=False)
    app_name = Column(String, nullable=False)
    cursor_position = Column(String, nullable=False)
    total_active_processes = Column(Integer, nullable=False)


def check_if_table_exists():
    print("checking if table exits")
    inspector = inspect(engine)
    if inspector.has_table(table_name):
        log.append("Table already exists. Not created again.\n")
    else:
        log.append("Table does not exist. Creating....")
        Base.metadata.create_all(engine)
        log.append("Successfully created the table.\n")

def save_to_buffer(q, observation):
    if q.size() > QUEUE_LEN:
        q.dequeue()
    q.enqueue(observation)

def housekeeping():
    Session = sessionmaker(bind=engine)
    session = Session()
    
    current_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    
    session.query(appinfo).filter(appinfo.timestamp.like(f"{current_date}%")).delete(synchronize_session=False)
    
    session.commit()
    session.close()

def clear_buffer(q):
    print("clearing buffer")
    temp = []
    current = q.front
    while current != None:
        current = current.next
        if current != None:
            temp.append(current.data)
    
    if temp:
        print('writing to db')
        Session = sessionmaker(bind=engine)
        session = Session()
        
        try: 
            session.bulk_insert_mappings(appinfo, temp)
            session.commit()
            temp.clear()
            print('wrote to db')
        except Exception as e:
            print(e)
            log.append(f"Exception occurred while writing to db: {e}\n")
            session.rollback()
        finally:
            session.close()
    else:
        print("Buffer is empty!") 
    