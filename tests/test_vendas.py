import unittest
from app.etl.venda import Vendas
from datetime import datetime
from unittest.mock import Mock, patch

class TestVendas(unittest.TestCase):

    def test_remove_empty_fields(self):
        self.assertEqual(Vendas.remove_empty_fields('    1    2     3     2,35'), ['',  '1', '2', '3','2.35'])

    def test_cpfcnpj_is_valid(self):
        # CPF tests
        self.assertEqual(Vendas.cpfcnpj_is_valid('12345678909', 'f'), (True, '123.456.789-09'))
        self.assertEqual(Vendas.cpfcnpj_is_valid('11111111111', 'f'), (False, '111.111.111-11'))
        self.assertEqual(Vendas.cpfcnpj_is_valid('', 'f'), (False, None))
        self.assertEqual(Vendas.cpfcnpj_is_valid('1234567890', 'f'), (False, '123.456.789-0'))
        # CNPJ tests
        self.assertEqual(Vendas.cpfcnpj_is_valid('12345678000195', 'j'), (True, '12.345.678/0001-95'))
        self.assertEqual(Vendas.cpfcnpj_is_valid('', 'j'), (False, None))
        self.assertEqual(Vendas.cpfcnpj_is_valid('1234567800019', 'j'), (False, '12.345.678/0001-9'))


    
    @patch('builtins.open', create=True)
    def test_load(self, mock_open):
        import tempfile
        import os
        from app.db.conection import Conection
        # Setup
        mock_open.return_value.__enter__.return_value.readlines.return_value = [
            "header1,header2,header3,header4,header5,header6,header7,header8\n",
            "12345678901,1,0,2021-12-01,1000.00,500.00,12345678000195,12345678000195\n",
            "12345678902,1,1,NULL,2000.00,1000.00,12345678000196,12345678000196\n"
        ]
        mock_conection = Mock()
        
        new_venda = Vendas()
        file_path = 'dummy_path.txt'
        
        # Call the method
        new_venda.load(file_path, mock_conection)

        # Assert
        self.assertEqual(mock_conection.save.call_count, 2)
        
        # Verify the first call
        args, kwargs = mock_conection.save.call_args_list[0]
        new_entry = args[0]
        self.assertEqual(new_entry.cpf, "123.456.789-01")
        self.assertTrue(new_entry.cpf_valido)
        self.assertEqual(new_entry.private, 1)
        self.assertEqual(new_entry.incompleto, 0)
        self.assertEqual(new_entry.data_ultima_compra, "2021-12-01")
        self.assertEqual(new_entry.ticket_medio, 1000.00)
        self.assertEqual(new_entry.ticket_medio_ultima_compra, 500.00)
        self.assertEqual(new_entry.loja_mais_frequente, "12.345.678/0001-95")
        self.assertTrue(new_entry.cnpj_valido)
        
        # Verify the second call
        args, kwargs = mock_conection.save.call_args_list[1]
        new_entry = args[0]
        self.assertEqual(new_entry.cpf, "123.456.789-02")
        self.assertTrue(new_entry.cpf_valido)
        self.assertEqual(new_entry.private, 1)
        self.assertEqual(new_entry.incompleto, 1)
        self.assertIsNone(new_entry.data_ultima_compra)
        self.assertEqual(new_entry.ticket_medio, 2000.00)
        self.assertEqual(new_entry.ticket_medio_ultima_compra, 1000.00)
        self.assertEqual(new_entry.loja_mais_frequente, "12.345.678/0001-96")
        self.assertTrue(new_entry.cnpj_valido)

