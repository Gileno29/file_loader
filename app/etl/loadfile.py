from unidecode import unidecode
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
import re
Base = declarative_base()

class Vendas(Base):
    __tablename__ = 'vendas'
    id = Column(Integer, primary_key=True)
    private = Column(String)
    incompleto = Column(String)
    ticket_medio = Column(String)
    ticket_medio_ultima_compra= Column(String)
    loja_mais_frequente= Column(String)
    loja_da_ultima_compra= Column(String)
    


"""
    funcao para mapear cabecalhos do arquivo explitado utilizando fatiamento

"""
normatize= lambda f: unidecode(f.strip().replace(' ', '_').lower())


def remove_empty_fields(self,data):
    return str(re.sub(",,{1,}",",",(str(data).replace(',','.').replace(' ',',')))).split(',')


'''def normatize_data(data):
    data_list=[]
    for d in data:
        data_list.append(d.split(' '))
    
    for list in data_list:
        for l in list:
            if l=='':
                data_list
    data_list=list(filter(is_not_empty_custom, data_list))
    print(data_list[0])'''

def recreate_table(self,tabela, engine, conection):
    tabela.drop(engine, checkfirst=True)  # Remove a tabela se ela existir
    tabela.create(engine)

def map_fields(self, fields):
    coluns=[normatize(fields[1:4]),
            normatize(fields[19:28]),
            normatize(fields[29:42]),
            normatize(fields[43:65]),
            normatize(fields[66:80]),
            normatize(fields[81:111]),
            normatize(fields[112:131]),
            normatize(fields[132:154])]
   
    #c=",".join([f"{colun[0],  colun[1]}".replace(',', '') for colun in coluns]).replace("('", '').replace("')",'').replace("'",'')
    #c=sinitize(c)
    #print(c)
    return coluns


def create_base(self, file_path, conection):
    with open(file_path, "r") as file:
        head_line = file.readline()
        conection.create(map_fields(head_line), 'vendas')

def load(self, file_path, conection):
    with open(file_path, "r") as file:
        lines= file.readlines()
        list_lines=[]
        for l in lines:
            #list_lines.append(l)
            print(remove_empty_fields(l))
            conection.save(remove_empty_fields(l), 'vendas')
            
#print(list_lines[1])
        #print(remove_empty_fields([list_lines[1]]))
        #conection.save(remove_empty_fields(list_lines), 'vendas')
        
        #for line in lines[1:]:
        #    print(line)
        #    break
        #print(no_empty_fields_list[1])

#load(file_path)



