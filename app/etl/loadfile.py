from unidecode import unidecode
import re
"""
    funcao para mapear cabecalhos do arquivo explitado utilizando fatiamento

"""
normatize= lambda f: unidecode(f.strip().replace(' ', '_').lower())




def normatize_data(data):
    data_list=[]
    for d in data:
        data_list.append(d.split(' '))
    
    for list in data_list:
        for l in list:
            if l=='':
                data_list
    data_list=list(filter(is_not_empty_custom, data_list))
    print(data_list[0])


def map_fields(fields):
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


def create_base(file_path, conection):
    with open(file_path, "r") as file:
        head_line = file.readline()
        conection.create(map_fields(head_line))

file_path='uploads/Base.txt'
def load(file_path, conection=None):
    with open(file_path, "r") as file:
        lines= file.readlines()
        normatize_data(lines[1:])
        #for line in lines[1:]:
        #    print(line)
        #    break

load(file_path)



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

