from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
from werkzeug.utils import secure_filename
import urllib.request
 
app = Flask(__name__)
 
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/styles/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
  
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     
@app.route('/')
def upload_form():
    return render_template('upload.html')
 
@app.route('/', methods=['POST'])
def upload_image():
    if 'files[]' not in request.files:
        flash('No file part')
        return redirect(request.url)
    files = request.files.getlist('files[]')
    file_names = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_names.append(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            flash('Allowed image types are -> png, jpg, jpeg')
            return redirect(request.url)
 
    return render_template('upload.html', filenames=file_names)
 
@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='styles/' + filename), code=301)
  
if __name__ == "__main__":
    app.run()
