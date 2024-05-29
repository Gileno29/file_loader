from flask import Flask,  request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

UPLOAD_FOLDER='uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

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
    file = request.files['arquivo1']
    print(request.files)
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

