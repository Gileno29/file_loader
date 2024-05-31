from unidecode import unidecode
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, Date, DECIMAL
import re
Base = declarative_base()

formats_cpf= lambda cpf : f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}" 
formats_cnpj = lambda cnpj : f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"
class Vendas(Base):
    __tablename__ = 'vendas'
    id = Column(Integer, primary_key=True)
    cpf= Column(String)
    private = Column(Integer)
    incompleto = Column(Integer)
    data_ultima_compra= Column(Date, nullable=True)
    ticket_medio = Column(DECIMAL(10, 2))
    ticket_medio_ultima_compra= Column(DECIMAL(10, 2))
    loja_mais_frequente= Column(String)
    loja_da_ultima_compra= Column(String)
    cpf_valido= Column(Boolean, default=True)
    cnpj_invalido= Column(Boolean, default=True)
    
    
    @staticmethod
    def remove_empty_fields(data):
        return str(re.sub(",,{1,}",",",(str(data).replace(',','.').replace(' ',',')))).split(',')

   
    @staticmethod
    def cpf_is_valid(cpfcnpj, t='f'):
        cpfcnpj = re.sub(r'\D', '', cpfcnpj)
        if t=='f':
            if cpfcnpj == cpfcnpj[0] * len(cpfcnpj):
                return False, formats_cpf(cpfcnpj)
            elif len(cpfcnpj)==11:
                return True, formats_cpf(cpfcnpj) 
            else:
                return False, formats_cpf(cpfcnpj)
        elif t=='j':
            if cpfcnpj == cpfcnpj[0] * len(cpfcnpj):
                return False, formats_cnpj(cpfcnpj)
            elif len(cpfcnpj) == 14:
                return False, formats_cnpj(cpfcnpj)
            else:
                return False, formats_cpf(cpfcnpj)


        
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
            


