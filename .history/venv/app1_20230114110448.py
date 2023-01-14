from flask import Flask, flash, request, redirect, render_template, send_from_directory, url_for
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired

# Flask Configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOADED_PHOTOS_DEST'] = 'static/files'

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

class UploadFileForm(FlaskForm):
    photo = FileField(validators=[
        FileAllowed(photos, 'Only images are allowed'),
        FileRequired('File field should not be empty')
    ])
    submit = SubmitField("Upload")

@app.route('/uploads/<filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'], filename)

# Upload single image of yourself
@app.route('/', methods=['GET',"POST"])
def upload_image():
    form = UploadFileForm()
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        file_url = url_for('get_file', filename=filename)
    else:
        file_url = None
    return render_template('index.html', form=form, file_url=file_url)

# Upload multiple images of desired style
app.config['UPLOAD_FOLDER'] = 'static/styles'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
  
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
 
@app.route('/', methods=['POST'])
def upload_images():
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
            flash('Allowed image types are -> png, jpg, jpeg, gif')
            return redirect(request.url)
 
    return render_template('upload.html', filenames=file_names)
 
@app.route('/display/<filename>')
def display_images(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)
  
if __name__ == "__main__":
    app.run()