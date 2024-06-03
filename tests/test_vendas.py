import unittest
from app.etl.venda import Vendas
from unittest.mock import Mock, patch
import unittest
import tempfile
import os
import uuid


"""
Mock para a classe de conexão real. 

Esta classe simula o comportamento da conexão real.
registra as entradas passadas para o método `save`
"""

class MockConnection(Mock):

    def __init__(self):
        super().__init__()
        self.saved_entries = []

    def save(self, new_entry):
        self.saved_entries.append(new_entry)

class TestVendas(unittest.TestCase):

    def test_remove_empty_fields(self):
        self.assertEqual(Vendas.remove_empty_fields('    1    2     3     2,35'), ['',  '1', '2', '3','2.35'])
        self.assertEqual(Vendas.remove_empty_fields('    5,25    2     8,00     2,35'), ['',  '5.25', '2', '8.00','2.35'])
        self.assertEqual(Vendas.remove_empty_fields('    0.00    2     22,50     2,35'), ['',  '0.00','2', '22.50','2.35'])

    def test_cpfcnpj_valid_format(self):
        # CPF tests
        self.assertEqual(Vendas.cpfcnpj_valid_format('12345678909', 'f'), (True, '123.456.789-09'))
        self.assertEqual(Vendas.cpfcnpj_valid_format('11111111111', 'f'), (False, '111.111.111-11'))
        self.assertEqual(Vendas.cpfcnpj_valid_format('', 'f'), (False, None))
        self.assertEqual(Vendas.cpfcnpj_valid_format('1234567890', 'f'), (False, '123.456.789-0'))
        # CNPJ tests
        self.assertEqual(Vendas.cpfcnpj_valid_format('12345678000195', 'j'), (True, '12.345.678/0001-95'))
        self.assertEqual(Vendas.cpfcnpj_valid_format('', 'j'), (False, None))
        self.assertEqual(Vendas.cpfcnpj_valid_format('1234567800019', 'j'), (False, '12.345.678/0001-9'))


      

    def test_load(self):
        with tempfile.NamedTemporaryFile() as tmpfile:
            """
            Testa a função load escrevendo dados de exemplo em um arquivo temporário,
            chamando a função load com o arquivo e uma conexão mock, e verificando
            se os dados foram carregados e salvos corretamente.
            """

            temp_filename = f"temp_file_{uuid.uuid4()}"
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.close()
                os.rename(temp_file.name, temp_filename)
                with open(temp_filename, "w") as f:
                    f.write("cpf_valido       cpf  private       incompleto    data_ultima_compra    ticket_medio   ticket_medio_ultima_compra    cnpj_valido  loja_mais_frequente   cnpj_valido   loja_da_ultima_compra\n")
                    f.write("12345678901   1  0    2023-10-04    100,50   50,25     12.345.678/0001-9  12.345.678/0001-9\n")
                    f.write("98765432109    0   1    2023-11-15    250.00   125.00       12.345.678/0001-95    12.345.678/0001-95\n")
                    f.write("98765432108    0   1    2023-11-18    250.00   125.00       12.345.678/0001-95    00.000.000/0000-00\n")

            mock_connection = MockConnection()
            new_venda=Vendas()
            new_venda.load(temp_filename, mock_connection)

            print(mock_connection.saved_entries)
            print(temp_filename)
            self.assertEqual(mock_connection.saved_entries[0].cpf_valido, True)
            self.assertEqual(mock_connection.saved_entries[0].cpf, "123.456.789-01")
            self.assertEqual(mock_connection.saved_entries[0].private, 1)
            self.assertEqual(mock_connection.saved_entries[0].incompleto, 0)
            self.assertEqual(mock_connection.saved_entries[0].data_ultima_compra, "2023-10-04")
            self.assertEqual(mock_connection.saved_entries[0].ticket_medio, 100.50)
            self.assertEqual(mock_connection.saved_entries[0].ticket_medio_ultima_compra, 50.25)
            self.assertEqual(mock_connection.saved_entries[0].loja_mais_frequente, '12.345.678/0001-9')
            self.assertEqual(mock_connection.saved_entries[0].loja_da_ultima_compra,'12.345.678/0001-9')
            self.assertEqual(mock_connection.saved_entries[0].cnpj_valido, False )

            self.assertEqual(mock_connection.saved_entries[1].cpf_valido, True)
            self.assertEqual(mock_connection.saved_entries[1].cpf, "987.654.321-09")
            self.assertEqual(mock_connection.saved_entries[1].private, 0)
            self.assertEqual(mock_connection.saved_entries[1].incompleto, 1)
            self.assertEqual(mock_connection.saved_entries[1].data_ultima_compra, "2023-11-15")
            self.assertEqual(mock_connection.saved_entries[1].ticket_medio, 250.00)
            self.assertEqual(mock_connection.saved_entries[1].ticket_medio_ultima_compra, 125.00)
            self.assertEqual(mock_connection.saved_entries[1].loja_mais_frequente, '12.345.678/0001-95')
            self.assertEqual(mock_connection.saved_entries[1].loja_da_ultima_compra,'12.345.678/0001-95')
            self.assertEqual(mock_connection.saved_entries[1].cnpj_valido, True )

            self.assertEqual(mock_connection.saved_entries[2].cpf_valido, True)
            self.assertEqual(mock_connection.saved_entries[2].cpf, "987.654.321-08")
            self.assertEqual(mock_connection.saved_entries[2].private, 0)
            self.assertEqual(mock_connection.saved_entries[2].incompleto, 1)
            self.assertEqual(mock_connection.saved_entries[2].data_ultima_compra, "2023-11-18")
            self.assertEqual(mock_connection.saved_entries[2].ticket_medio, 250.00)
            self.assertEqual(mock_connection.saved_entries[2].ticket_medio_ultima_compra, 125.00)
            self.assertEqual(mock_connection.saved_entries[2].loja_mais_frequente, '12.345.678/0001-95')
            self.assertEqual(mock_connection.saved_entries[2].loja_da_ultima_compra,'00.000.000/0000-00')
            self.assertEqual(mock_connection.saved_entries[2].cnpj_valido, False )
            os.remove(temp_filename)
