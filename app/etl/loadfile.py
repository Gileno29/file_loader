import pandas as pd
from db import conection
from unidecode import unidecode

def map_fields(fields):
    coluns=[unidecode(fields[1:4].strip().replace(' ', '_').lower()),
            unidecode(fields[19:28].strip().replace(' ', '_').lower()),
            unidecode(fields[29:42].strip().replace(' ', '_').lower()),
            unidecode(fields[43:65].strip().replace(' ', '_').lower()),
            unidecode(fields[66:80].strip().replace(' ', '_').lower()),
            unidecode(fields[81:111].strip().replace(' ', '_').lower()),
            unidecode(fields[112:131].strip().replace(' ', '_').lower()),
            unidecode(fields[132:154].strip().replace(' ', '_').lower())]

    return coluns



file_path = "../uploads/Base.txt"
file_lines=''
coluns=''
with open(file_path, "r") as arquivo:
	file_lines = arquivo.readlines()


for line in file_lines:
      coluns=map_fields(line)
      con=conection.connect()
      for c in coluns:
            
      con.execute("create table vendas ("+ )
      break


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