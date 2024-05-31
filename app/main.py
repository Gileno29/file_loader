from flask import Flask,  request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from app.etl import loadfile
from app.db import conection
import os

app = Flask(__name__)

UPLOAD_FOLDER='uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def hello_world():
      return '''
   <!doctype html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Upload de Arquivo</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background-color: #f4f4f9;
        }
        .upload-container {
            background-color: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            text-align: center;
        }
        h1 {
            color: #333;
        }
        input[type="file"] {
            margin: 20px 0;
        }
        input[type="submit"] {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        input[type="submit"]:hover {
            background-color: #45a049;
        }
    </style>
</head>
<body>
    <div class="upload-container">
        <h1>Envie seu arquivo</h1>
        <form method="post" enctype="multipart/form-data" action="/upload">
            <input type="file" name="file" required>
            <input type="submit" value="Upload">
        </form>
    </div>
</body>
</html>
'''  


@app.route("/upload", methods=['POST', 'GET'])
def upload():
    file = request.files['file']
    #print(request.files)
    if file:
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      #print("Caminho: ", str(os.path.join(app.config['UPLOAD_FOLDER'], filename)))
      new_conection=conection.Conection()
      new_venda= loadfile.Vendas()
      new_conection.drop_table(new_venda)
      #print(new_venda)
      new_venda.load(str(os.path.join(app.config['UPLOAD_FOLDER'], filename)), new_conection)

