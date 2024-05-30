import os
from dotenv import load_dotenv
from sqlalchemy import create_engine,  Table, Column, String, Integer, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData

class Conection:
    def __init__(self, db_host=None, db_database=None, db_user=None, db_pasword=None, db_port=None):
        load_dotenv()
        self.host = os.getenv('DB_HOST') if not db_host else db_host
        self.database = os.getenv('DB_DATABASE') if not db_database else db_database
        self.user = os.getenv('DB_USER') if not db_user else db_user
        self.password = os.getenv('DB_PASSWORD') if not db_pasword else db_pasword
        self.port = os.getenv('DB_PORT') if not db_port else db_port
    def create(self, columns):
        db_url = f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
        engine = create_engine(db_url)
        
        metadata_obj = MetaData()
        cols = []
        for col_name in columns:  
            cols.append(Column(col_name, String(255)))

        #print(cols)
        metadata = Table('vendas',metadata_obj,*cols, schema='public')
        #metadata.create_all(engine)
        metadata_obj.create_all(engine)
    


