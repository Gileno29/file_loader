import unittest
from app.etl.venda import Vendas
from unittest.mock import Mock, patch
import unittest
import tempfile
import os
import uuid
import pandas as pd


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

    def test_make_list_empty(self):
        """ Testa se a função funciona com uma lista vazia. """
        origin_list = []
        expected_list = []
        self.assertEqual(Vendas.make_list(origin_list),expected_list)
    
    def test_make_list_with_file(self):
        """
            Testa a função make_list escrevendo dados de exemplo em um arquivo temporário,
            verificando se os dados retornam no formato esperado.
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
        
        
        for bloco in pd.read_csv(temp_filename, chunksize=3000,sep='\t',skiprows=1, iterator=True, header=None):
        
            expected_first_element =['12345678901','1','0','2023-10-04','100.50','50.25','12.345.678/0001-9','12.345.678/0001-9']
            expected_second_element =['98765432109','0', '1', '2023-11-15', '250.00', '125.00', '12.345.678/0001-95', '12.345.678/0001-95']
            expected_third_element=['98765432108','0','1','2023-11-18','250.00','125.00','12.345.678/0001-95', '00.000.000/0000-00']
            origin_list=Vendas.make_list(bloco.values.tolist())
            self.assertEqual(origin_list[0], expected_first_element)
            self.assertEqual(origin_list[1], expected_second_element)
            self.assertEqual(origin_list[2], expected_third_element)
            os.remove(temp_filename)

   
    
    def test_valid_cpf_cnpj(self):
        """
        Testa a função de validação de cpfs/cnpjs através de comparações de entrada e saida.
        """
        self.assertEqual(Vendas.valid_cpf_cnpj('12345678909', 'f'), (True, '123.456.789-09'))
        self.assertEqual(Vendas.valid_cpf_cnpj('11111111111', 'f'), (False, '111.111.111-11'))
        self.assertEqual(Vendas.valid_cpf_cnpj('', 'f'), (False, None))
        self.assertEqual(Vendas.valid_cpf_cnpj('52381815155', 'f'), (True, '523.818.151-55'))
    

        self.assertEqual(Vendas.valid_cpf_cnpj('23809070000190', 'j'), (True, '23.809.070/0001-90'))
        self.assertEqual(Vendas.valid_cpf_cnpj('', 'j'), (False, None))
        self.assertEqual(Vendas.valid_cpf_cnpj('1234567800019', 'j'), (False, '12.345.678/0001-9'))


      
    @patch('app.etl.venda.Vendas.save_object')
    def test_load(self, mock_save_object):
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
        mock_save_object.assert_called_once()
        os.remove(temp_filename)
           
  