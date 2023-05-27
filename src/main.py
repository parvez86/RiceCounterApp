import logging

import flask
import numpy as np
import cv2
from flask_ngrok import run_with_ngrok
from flask import Flask, request, render_template
from joblib import load
from model import MyModel
from json import dumps
import io
import base64
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import datetime
from PIL import Image

app = Flask(__name__, template_folder='./templates')
UPLOAD_FOLDER = '../uploads'
app.secret_key = "sp86.12345"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
run_with_ngrok(app)

ALLOWED_EXTENSIONS = set({"png", "jpg", "jpeg"})


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'files' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['files']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            file.filename = str(datetime.datetime.now()).replace('.', '-')+'.'+file.filename.rsplit(".", 1)[1].lower()
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            img = np.array(Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename)))
            model = MyModel()
            res = model.process_image([img])
            res[0]['path'] = {
                'image_path': UPLOAD_FOLDER+'/'+filename
            }
            print('output: ', res[0])
            return render_template('index.html', output=res[0])

    return render_template('index.html')


if __name__ == '__main__':
    app.run()
