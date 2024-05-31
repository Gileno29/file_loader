import os
from dotenv import load_dotenv
from sqlalchemy import create_engine,  Table, Column, String, Integer, inspect, insert
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker

class Conection:
    def __init__(self):
        load_dotenv()
        self.host = os.getenv('DB_HOST') 
        self.database = os.getenv('DB_DATABASE') 
        self.user = os.getenv('DB_USER') 
        self.password = os.getenv('DB_PASSWORD') 
        self.port = os.getenv('DB_PORT')
        self.db_url=f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

    def create(self, table):
        engine = create_engine(self.db_url)
        table.metadata.create_all(engine)
    
    def save(self, data, table):
        engine = create_engine(self.db_url)
        print(data)
        s = sessionmaker(bind=engine)
        session = s()
        session.add(data)
        session.commit()
  
    def drop_table(self, table):
        engine = create_engine(self.db_url)
        table.__table__.drop(engine, checkfirst=True)
        table.__table__.create(engine)
        


