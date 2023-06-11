from flask import Flask, render_template, flash, request, redirect
import os
from werkzeug.utils import secure_filename
import model_code

UPLOAD_PATH = './static/'
ALLOWED_EXTENSIONS = set(['tiff', 'bpm', 'png', 'jpg', 'jpeg', 'gif'])
app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def homepage():
    return render_template('home.html')

@app.route('/', methods=['POST'])
def segment():
    if request.method == 'POST':
        for f in os.listdir(UPLOAD_PATH):
            os.remove(os.path.join(UPLOAD_PATH, f))
        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)
        files = request.files.getlist('files[]')
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(UPLOAD_PATH + file.filename)
                currentPath = UPLOAD_PATH + file.filename
                file = model_code.process_image_and_predict(currentPath)
                file.save(currentPath)
        return redirect('/results')


@app.route('/results')
def results():
    image_files = [f for f in os.listdir(UPLOAD_PATH) if os.path.isfile(os.path.join(UPLOAD_PATH, f))]
    return render_template('results.html', image_files=image_files)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
