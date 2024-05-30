import os
from dotenv import load_dotenv
from sqlalchemy import create_engine,  Table, Column, String, Integer, inspect, insert
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker

class Conection:
    def __init__(self, db_host=None, db_database=None, db_user=None, db_pasword=None, db_port=None):
        load_dotenv()
        self.host = os.getenv('DB_HOST') if not db_host else db_host
        self.database = os.getenv('DB_DATABASE') if not db_database else db_database
        self.user = os.getenv('DB_USER') if not db_user else db_user
        self.password = os.getenv('DB_PASSWORD') if not db_pasword else db_pasword
        self.port = os.getenv('DB_PORT') if not db_port else db_port
    def create(self, columns, table):
        db_url = f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
        engine = create_engine(db_url)
        metadata_obj = MetaData()
        cols = []
        for col_name in columns:  
            cols.append(Column(col_name, String(255)))

        #print(cols)
        metadata = Table(table,metadata_obj,*cols, schema='public')

        metadata_obj.create_all(engine)
    
    def save(self, data, table):
        db_url = f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
        engine = create_engine(db_url)

        Session = sessionmaker(bind=engine)
        session = Session()
        insert=table(*data)
        session.add(insert)
        session.commit()


