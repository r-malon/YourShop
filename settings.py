from flask import *
from playhouse.shortcuts import model_to_dict, dict_to_model
from werkzeug.utils import secure_filename
import os

with open('SECRET_KEY', encoding='utf-8') as f:
	SECRET_KEY = f.read()

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'gif', 'webp', 'tiff'} # set

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_ext(filename):
	return filename.rsplit('.', 1)[1].lower()
