from datetime import datetime, timedelta
from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker

from .config import TABLE_NAME, appinfo, Base, engine

log = []

def check_if_table_exists():
    print("checking if table exits")
    inspector = inspect(engine)
    if inspector.has_table(TABLE_NAME):
        log.append("Table already exists. Not created again.\n")
    else:
        log.append("Table does not exist. Creating....")
        Base.metadata.create_all(engine)
        log.append("Successfully created the table.\n")

def housekeeping():
    current_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    
    Session = sessionmaker(bind=engine)
    session = Session()
    session.query(appinfo).filter(appinfo.timestamp.like(f"{current_date}%")).delete(synchronize_session=False)
    session.commit()
    session.close()

def write_to_db(q):
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
        print("Cache is empty!") 
    