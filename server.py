from msilib.schema import File
from flask import Flask, request, Response
from werkzeug.utils import secure_filename
import cv2 as cv
from PIL import Image
import os
from SuperResolution import SuperResolution

UPLOAD_FOLDER = './static/input_images/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           
@app.route('/')
def index():
    return "Hello World!"

@app.route("/upload_image", methods=["POST"])
def uploadImage():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'picture' not in request.files:
            return "Error"
        
        file = request.files['picture']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return "Error"
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            image_path= os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(image_path)
            
            sr= SuperResolution()
            sr.predict(image_path, filename)
        
            return "Image Uploaded!", 200
    
if __name__=="__main__":
    app.run()