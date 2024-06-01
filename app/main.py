from flask import Flask,  request, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
from app.etl import venda
from app.db import conection
import os

app = Flask(__name__)

UPLOAD_FOLDER=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def hello_world():
      return render_template('index.html')


@app.route("/upload", methods=['POST'])
def upload():

    if request.method == 'POST':
        print("o metodo é o post")
        if 'file' not in request.files:
            return 'No file part', 400
        
        
    file = request.files['file']
    if file:
      filename = secure_filename(file.filename)
      try:
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      except Exception as e:
          print("Erro ao salvar", e)
      new_conection=conection.Conection()
      new_venda= venda.Vendas()
      new_conection.drop_table(new_venda)
      new_venda.load(str(os.path.join(app.config['UPLOAD_FOLDER'], filename)), new_conection)



