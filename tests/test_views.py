import unittest
import json
from unittest.mock import Mock, patch, MagicMock
from app.main import app,   allowed_file, process_file, status, conection
from app.db.conection import Conection  
from app.etl.venda import Venda 
from flask import Flask, render_template, redirect, url_for
from io import BytesIO
import os




class TestViews(unittest.TestCase):
    
    def test_list_records_success__view(self):
        """
        Testa a view de listagem de registros fazendo um mock do retorno dos dados
        e testando se retornaram de forma correta
        """
        with app.test_client() as client:
            with patch.object(Conection, 'list_all') as mock_list_all:
                mock_list_all.return_value = [
                    (1, "123.456.789-01", 0, 1, "2023-10-04", 100.50, 50.25, "12.345.678/0001-9", "12.345.678/0001-9", True, True)
                ]

                response = client.get('/list_records')

                self.assertEqual(response.status_code, 200)

                data = json.loads(response.data)
                self.assertEqual(len(data), 1)
                self.assertEqual(data['0']['id'], 1)
                self.assertEqual(data['0']['cpf'], "123.456.789-01")
                self.assertEqual(data['0']['private'], 0)

    
          
    def test_list_records_no_data_view(self):
        """
        Testa a view de listagem de registros quando não deve retornar nenhum valor
        """   
        with app.test_client() as client:

            with patch.object(Conection, 'list_all') as mock_list_all:
                mock_list_all.return_value = None

                response = client.get('/list_records')

                self.assertEqual(response.status_code, 400)

                data = json.loads(response.data)

                self.assertEqual(data['message'], "No records found")
                self.assertEqual(data['status_code'], 400)
   
       
    def test_index_view(self):
        """
        Valida status de retorno da view index
        """  
        response = app.test_client().get('/')
        self.assertEqual(response.status_code, 200)



    def test_load_view(self):
        """
        Valida retorno da view de loading 
        """  
        response = app.test_client().get('/loading')   
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.url, 'http://localhost/loading')
    
     
    def test_status_view(self):
        """
        Valida retorno da view de status 
        """ 
        response = app.test_client().get('/status')   
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.url, 'http://localhost/status')
    
        
   
    def test_upload_no_file(self):
        """
        Valida retorno da view de upload de arquivo quando não é enviado arquivo 
        """  
        response = app.test_client().post('/upload')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'No file', response.data)


   
    @patch('app.main.process_file')
    def test_upload_allowed_file(self, mock_process_file):
        """
        Valida retorno da view de upload quando enviado um arquivo, criar um arquivo
        temporario que deve ser removido ao final da execução 
        """
        data = {
            'file': (BytesIO(b'my file contents'), 'test.txt')
        }
        response = app.test_client().post('/upload', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 302)
        mock_process_file.assert_called_once()
        os.remove(str(app.config['UPLOAD_FOLDER'])+'/test.txt')

   
    def test_upload_disallowed_file(self):
        """
        Valida retorno da view de upload quando enviado um arquivo que não está dentro das extensões permitidas
        """
        data = {
            'file': (BytesIO(b'my file contents'), 'test.exe')
        }
        response = app.test_client().post('/upload', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 403)
