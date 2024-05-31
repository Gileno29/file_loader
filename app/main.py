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
    <title>Upload de Arquivo</title>
    <h1>Envie seu arquivo</h1>
    <form method=post enctype=multipart/form-data action=/upload>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>'''  


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

