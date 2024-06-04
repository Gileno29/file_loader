from unidecode import unidecode
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, Date, DECIMAL
from flask import Flask,  request, render_template
import pandas as pd
import re
import threading
Base = declarative_base()
formats_cpf= lambda cpf : f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}" 
formats_cnpj = lambda cnpj : f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"
class Venda(Base):
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
    def make_list(origin_list):
            """
                Converte uma string para uma lista.
                Args:
                    origin_list (list): A lista original a ser convertida. Elementos podem ser strings ou outros iteráveis.

                Returns:
                    list: Uma nova lista onde cada elemento é uma sublista contendo os elementos originais transformados em floats.

                Observações:
                    - Substitui vírgulas (',') por pontos ('.') para conversão adequada para floats.
                    - Remove todos os espaços em branco para garantir valores delimitados corretamente.
                    - Remove aspas simples iniciais e finais ([' e ']) e separa os elementos por vírgulas.
            """
            changed_list = []
            for string in origin_list:
                string=str(string).replace(',', '.')
                string = re.sub(r"\s+", ",", str(string))
                sublist = string.replace("['","").replace("']", "").split(',')
                changed_list.append(sublist)
            return changed_list
   
   

    @staticmethod
    def valid_cpf_cnpj(cpf_cnpj, t='f'):
        """
        Valida e formata um CPF ou CNPJ.

        Args:
            cpf_cnpj (str): O CPF ou CNPJ a ser validado e formatado.
            t (str, optional): Tipo de documento a ser validado. Padrão é 'f' para CPF.
                - 'f': Valida e formata um CPF.
                - 'j': Valida e formata um CNPJ.

        Returns:
                 Uma tupla contendo dois elementos.
                - bool: True se o CPF/CNPJ for válido, False caso contrário.
                - str (opcional): O CPF/CNPJ formatado  mesmo com digitos incompletos, ou None caso o campo seja completamente vazio.
        """
        cpf_cnpj = re.sub(r'\D', '', cpf_cnpj)
        if t=='f':
            if cpf_cnpj =='':
                return False, None
            if len(cpf_cnpj) != 11 or cpf_cnpj in [str(i) * 11 for i in range(10)]:
                return False, formats_cpf(cpf_cnpj)
            
            for i in range(9, 11):
                s = sum(int(cpf_cnpj[num]) * (i+1-num) for num in range(0, i))
                dg = (s * 10 % 11) % 10
                if dg != int(cpf_cnpj[i]):
                    return False, formats_cpf(cpf_cnpj)
            return True, formats_cpf(cpf_cnpj)
                

        elif t=='j':
            if cpf_cnpj =='':
                return False, None
            if len(cpf_cnpj) != 14 or cpf_cnpj in [str(i) * 14 for i in range(10)]:
                return False, formats_cnpj(cpf_cnpj)
            p1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
            p2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

            def calc_digit(cnpj, p):
                s = sum(int(cnpj[i]) * p[i] for i in range(len(p)))
                r = s % 11
                return 0 if r < 2 else 11 - r

            d1 = calc_digit(cpf_cnpj[:-2], p1)
            d2 = calc_digit(cpf_cnpj[:-2] + str(d1), p2)
            if cpf_cnpj[-2:]!=f"{d1}{d2}":
                return False, formats_cnpj(cpf_cnpj)
            
            return True, formats_cnpj(cpf_cnpj)
        
            

    def save_object(self,df, conection):
        """
        Recupera os dados de Vendas de um DataFrame para o banco de dados.

        Argumentos:
            df (pandas.DataFrame): O DataFrame contendo dados de clientes.
            connection (object): Objeto de conexão com o banco de dados.

        Retorno:
            Nenhum

        Observações:
            - Valida e transforma os dados antes de salvá-los.
            - Manipula valores ausentes de forma adequada.
        """
  
        for line in list(df):
                new_entry=Venda()
                new_entry.cpf_valido,new_entry.cpf=self.valid_cpf_cnpj(line[0])
                new_entry.private=int(line[1])
                new_entry.incompleto=int(line[2])
                new_entry.data_ultima_compra=line[3] if line[3]!='NULL' else None
                new_entry.ticket_medio=float(line[4]) if line[4]!='NULL' else 0.00
                new_entry.ticket_medio_ultima_compra=float(line[5]) if line[5]!='NULL' else 0.00
                new_entry.cnpj_valido, new_entry.loja_mais_frequente= self.valid_cpf_cnpj(line[6], 'j')
                new_entry.cnpj_valido, new_entry.loja_da_ultima_compra= self.valid_cpf_cnpj(line[7], 'j')

                conection.save(new_entry)

                
    def load(self, file_path, conection):  
        """
        Carrega um arquivo de dados delimitado e o salva no banco de dados usando threads paralelas.

        Argumentos:
            file_path (str): Caminho para o arquivo de dados delimitado.
            connection (object): Objeto de conexão com o banco de dados.

        Retorno:
            Nenhum
        """
        threads = []      
        for bloco in pd.read_csv(file_path, chunksize=3000,sep='\t',skiprows=1, iterator=True, header=None):
            thread=threading.Thread(target=self.save_object, args=(self.make_list(bloco.values.tolist()), conection))
            thread.start()
            threads.append(thread)
       
        for thread in threads:
            thread.join()


       