from flask import Flask,  request, render_template, jsonify, redirect, url_for, flash
from werkzeug.utils import secure_filename
from app.etl import venda
from app.db import conection
import threading
import os

app = Flask(__name__)

UPLOAD_FOLDER=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'txt'}
status={}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_file(file_path, conection):
    new_venda = venda.Vendas()
    new_venda.load(file_path, conection)
    status['processing'] = False
    status['done'] = True

@app.route("/")
def index():
      return render_template('index.html')


@app.route("/upload", methods=['POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file ', 400
    
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        try:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        except Exception as e:
            print("Erro ao salvar", e)
            return 'Erro ao salvar o arquivo', 500
        
        status['processing'] = True
        status['done'] = False
        new_conection=conection.Conection()
        try:
            threading.Thread(target=process_file, args=(file_path, new_conection)).start()
        except Exception as e:
            print("Erro ao startar Thread", e)
            
        return redirect(url_for('loading'))


@app.route('/loading')
def loading():
    return render_template('loading.html')

@app.route('/status')
def get_status():
    return jsonify(status)

@app.route('/reset_db')
def reset_db():
    new_conection=conection.Conection()
    new_venda=venda.Vendas()
    new_conection.recreate_table(new_venda)
    return redirect(url_for('index'))

@app.route('/list_records')
def list_records():
    new_conection=conection.Conection()
    new_venda=venda.Vendas()
    print("o retorno da funcao", new_conection.list_all(new_venda))
    return jsonify(new_conection.list_all(new_venda))
    
    