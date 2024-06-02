from unidecode import unidecode
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, Date, DECIMAL
from flask import Flask,  request, render_template
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
    cnpj_valido= Column(Boolean, default=True)
    
    
   
   
    @staticmethod
    def remove_empty_fields(data):
        return str(re.sub(",,{1,}",",",(str(data).replace(',','.').replace(' ',',')))).split(',')

   

    @staticmethod
    def cpfcnpj_is_valid(cpfcnpj, t='f'):
        cpfcnpj = re.sub(r'\D', '', cpfcnpj)
        if t=='f':
            if cpfcnpj =='':
                return False, None
            elif cpfcnpj == cpfcnpj[0] * len(cpfcnpj):
                return False, formats_cpf(cpfcnpj)
            elif len(cpfcnpj)==11:
                return True, formats_cpf(cpfcnpj) 
            else:
                return False, formats_cpf(cpfcnpj)
        elif t=='j':
            if cpfcnpj =='':
                return False, None
            elif cpfcnpj == cpfcnpj[0] * len(cpfcnpj):
                return False, formats_cnpj(cpfcnpj)
            elif len(cpfcnpj) == 14:
                return True, formats_cnpj(cpfcnpj)
            else:
                return False, formats_cnpj(cpfcnpj)
        

    def load(self, file_path, conection):
        with open(file_path, "r") as file:
            lines= file.readlines()
            for l in lines[1:]:
                fields=self.remove_empty_fields(l)
                
                new_entry=Vendas()
                new_entry.cpf_valido,new_entry.cpf=self.cpfcnpj_is_valid(fields[0])
                new_entry.private=int(fields[1])
                new_entry.incompleto=int(fields[2])
                new_entry.data_ultima_compra=fields[3] if fields[3]!='NULL' else None
                new_entry.ticket_medio=float(fields[4]) if fields[4]!='NULL' else 0.00
                new_entry.ticket_medio_ultima_compra=float(fields[5]) if fields[5]!='NULL' else 0.00
                new_entry.cnpj_valido, new_entry.loja_mais_frequente= self.cpfcnpj_is_valid(fields[6], 'j')
                new_entry.cnpj_valido, new_entry.loja_da_ultima_compra= self.cpfcnpj_is_valid(fields[7], 'j')

                conection.save(new_entry)
