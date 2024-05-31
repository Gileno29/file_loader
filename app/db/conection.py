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
    def create(self, columns=None, table=None):
        engine = create_engine(self.db_url)
        table.create(engine)
        ''''metadata_obj = MetaData()'''
        '''cols = []'''
    '''for col_name in columns:  
            cols.append(Column(col_name, String(255)))

        #print(cols)
        Table(table,metadata_obj,*cols, schema='public')

        metadata_obj.create_all(engine)'''
    
    def save(self, data, table):
        engine = create_engine(self.db_url)
        Session = sessionmaker(bind=engine)
        session = Session()
        metadata= MetaData()
        my_table=Table(table, metadata, autoload_with=engine)
        print(data)
        insert_query = my_table.insert().values(data)
        session.execute(insert_query)
        session.commit()
  
    def drop_table(self, table):
        engine = create_engine(self.db_url)
        table.drop(engine, checkfirst=True)
        tabela.create(engine)
        


