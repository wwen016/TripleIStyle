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

@app.route('/display/<filename>')
def display_image(filename):
	#print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)

if __name__ == "__main__":
    app.run()

# import requests, os, re
# from flask import Flask,redirect,url_for,render_template,request
# from werkzeug.utils import secure_filename           # Used to store filename

# app=Flask(__name__)

# @app.route("/")
# def uploader():
#         path = 'static/uploads/'
#         uploads = sorted(os.listdir(path), key=lambda x: os.path.getctime(path+x))        # Sorting as per image upload date and time
#         print(uploads)
#         #uploads = os.listdir('static/uploads')
#         uploads = ['uploads/' + file for file in uploads]
#         uploads.reverse()
#         return render_template("index.html",uploads=uploads)            # Pass filenames to front end for display in 'uploads' variable

# app.config['UPLOAD_PATH'] = 'static/uploads'             # Storage path    
# @app.route("/upload",methods=['GET','POST'])
# def upload_file():                                       # This method is used to upload files 
#         if request.method == 'POST':
#                 f = request.files['file']
#                 print(f.filename)
#                 #f.save(secure_filename(f.filename))
#                 filename = secure_filename(f.filename)
#                 f.save(os.path.join(app.config['UPLOAD_PATH'], filename))
#                 return redirect("/")           # Redirect to route '/' for displaying images on fromt end

# if __name__=="__main__":
#     app.run()