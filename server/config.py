import json
import os

from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String

print(os.getcwd())
config_file = os.path.join(os.path.dirname(__file__), 'config.json')
with open(config_file, 'r') as f:
    config = json.load(f)
print(config)

if not os.path.exists('data'):
    os.mkdir('data')

OBSERVATION_INTERVAL = config["observation_interval"]
DB_PATH = 'data/' + config['db_name']
TABLE_NAME = config['table_name']
QUEUE_LEN = config['queue_len']

#sql engine
Base = declarative_base()
connected_args = {'check_same_thread': False}
engine = create_engine(f'sqlite:///{DB_PATH}',
                       connect_args=connected_args)
with engine.connect():
    pass

#sql data model
class appinfo(Base):
    __tablename__ = 'app_data'
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(String, nullable=False)
    total_active_processes = Column(Integer, nullable=False)
    app_name = Column(String, nullable=False)
    cursor_position = Column(String, nullable=False)
