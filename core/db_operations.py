from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy import inspect
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import String
import os

DB_DIR = os.path.join(os.path.dirname(__file__), '..','data')
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, 'system_monitoring.db')
TABLE_NAME = 'app_data'

QUEUE_LEN = 50
log = []

Base = declarative_base()
engine = create_engine(rf'sqlite:///{DB_PATH}')

def db_init():
    with engine.connect():
        pass

class appinfo(Base):
    __tablename__ = TABLE_NAME
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(String, nullable=False)
    app_name = Column(String, nullable=False)
    cursor_position = Column(String, nullable=False)
    total_active_processes = Column(Integer, nullable=False)


def check_if_table_exists():
    print("checking if table exits")
    inspector = inspect(engine)
    if inspector.has_table(TABLE_NAME):
        log.append("Table already exists. Not created again.\n")
    else:
        log.append("Table does not exist. Creating....")
        Base.metadata.create_all(engine)
        log.append("Successfully created the table.\n")

def save_to_buffer(q, observation):
    if q.size > QUEUE_LEN:
        q.dequeue()
    print(q.size)
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
    