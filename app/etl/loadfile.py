from unidecode import unidecode
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
import re
Base = declarative_base()

class Vendas(Base):
    __tablename__ = 'vendas'
    id = Column(Integer, primary_key=True)
    cpf= Column(String)
    private = Column(String)
    incompleto = Column(String)
    data_ultima_compra= Column(String)
    ticket_medio = Column(String)
    ticket_medio_ultima_compra= Column(String)
    loja_mais_frequente= Column(String)
    loja_da_ultima_compra= Column(String)
    
    def remove_empty_fields(self,data):
        return str(re.sub(",,{1,}",",",(str(data).replace(',','.').replace(' ',',')))).split(',')

    def recreate_table(self,tabela, engine, conection):
        tabela.drop(engine, checkfirst=True) 
        tabela.create(engine)

    def load(self, file_path, conection):
        with open(file_path, "r") as file:
            lines= file.readlines()
            count=0
            for l in lines:
                count+=1
                if count==1:
                    continue
                fields=self.remove_empty_fields(l)
                new_entry=Vendas(cpf=fields[0],private=fields[1],
                                incompleto=fields[2],data_ultima_compra=fields[3],
                                ticket_medio=fields[4], ticket_medio_ultima_compra=fields[5],
                                loja_mais_frequente=fields[6],
                                loja_da_ultima_compra=fields[7] )

                conection.save(new_entry, self.__tablename__)
            


