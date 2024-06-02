import re
cpfcnpj = re.sub(r'\D', '', '11.111.111/0001-11')
print(cpfcnpj)
if cpfcnpj == cpfcnpj[0] * len(cpfcnpj):
    print("cpfcnpj sem caracteres: ", cpfcnpj)
