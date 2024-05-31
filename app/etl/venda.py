from unidecode import unidecode
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean
import re
Base = declarative_base()

formats_cpf= lambda cpf : f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
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
    cpf_valido= Column(Boolean, default=True)
    
    def remove_empty_fields(self,data):
        return str(re.sub(",,{1,}",",",(str(data).replace(',','.').replace(' ',',')))).split(',')

    def recreate_table(self,table, engine, conection):
        table.drop(engine, checkfirst=True) 
        table.create(engine)
   
    @staticmethod
    def cpf_is_valid(cpf):
        cpf = re.sub(r'\D', '', cpf)
        if cpf == cpf[0] * len(cpf):
            return False, formats_cpf(cpf)
        
        elif len(cpf)==11:
            return True, formats_cpf(cpf)
        
        else:
            return False, formats_cpf(cpf)

        
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
                valid, cpf=self.cpf_is_valid(new_entry.cpf)
                new_entry.cpf = cpf
                new_entry.cpf_valido=valid

                conection.save(new_entry, self.__tablename__)
            


