# app.py
from flask import Flask, request, render_template, jsonify
import os
from werkzeug.utils import secure_filename
import pathlib
from fastai.learner import load_learner
from PIL import Image
import numpy as np

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        temp = pathlib.PosixPath
        pathlib.PosixPath = pathlib.WindowsPath

        # Use forward slashes for paths in Windows
        model_path = r'trained_model'

        learn = load_learner(model_path)

        print("model is successfully loaded")

        try:
            img = Image.open(filepath)
            img = img.resize((128, 128))
            img = img.convert('RGB')
            img_array = np.array(img)

            # Use the learner/model to make a prediction on the image_array
            prediction = learn.predict(img_array)
            result = str(prediction)
            if 'benign' in result:
                result = "Benign"
            else:
                result = "Malignant"
            return jsonify({'result': result})

        except Exception as e:
            return jsonify({'error': f'Error: {str(e)}'})

    return jsonify({'error': 'Invalid file format'})


if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
