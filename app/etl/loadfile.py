import pandas as pd
from db import conection
from unidecode import unidecode

normatize= lambda f: unicode(f.strip().replace(' ', '_').lower())
def map_fields(fields):
    coluns=[(normatize(fields[1:4]), "VARCHAR(255)"),
            (normatize(fields[19:28]), "VARCHAR(255)"),
            (normatize(fields[29:42]), "VARCHAR(255)"),
            (normatize(fields[43:65]), "VARCHAR(255)"),
            (normatize(fields[66:80]), "VARCHAR(255)"),
            (normatize(fields[81:111]), "VARCHAR(255)"),
            (normatize(fields[112:131]), "VARCHAR(255)"),
            (normatize(fields[132:154]), "VARCHAR(255)")]

    return coluns



file_path = "../uploads/Base.txt"
file_lines=''
coluns=''

def create_base(file_path):
    with open(file_path, "r") as arquivo:
        head_line = arquivo.readline()
        coluns=map_fields(head_line)
        
        sql= f"""
            DROP TABLE IF EXISTS vendas;
            CREATE TABLE vendas(
                {",".join([f"{colun[0], colun[1]}" for colun in coluns])}
            );"""
        try:
            con=conection.connect()
            con.execute(sql)
        except Exception as e:
            print("Error in table creation: ", e)
        con.close()


def load():
    pass


'''
df = pd.read_csv(file_path, delimiter='\t')

print(df.head())

header = pd.read_csv(file_path, delimiter='\0', nrows=2)
column_names = header.columns.tolist()
print(str(column_names))


cpf=str(column_names)[3:7]
print(cpf)

#test=str(column_names).split('\t')
#print(test)
'''