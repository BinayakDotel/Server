from msilib.schema import File
from flask import Flask, request, Response
from werkzeug.utils import secure_filename
import os
from SuperResolution import SuperResolution
import base64

UPLOAD_FOLDER = './static/input_images/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

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
    if 'picture' not in request.files:
        return "Error"
    file = request.files['picture']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        return {"error":"No file added"}, 400
    if file and allowed_file(file.filename):
        try:
            filename = secure_filename(file.filename)
            image_path= os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(image_path)
            sr = SuperResolution()
            sr.predict(image_path, filename)
            with open("./static/output_images/enhanced_"+filename, 'rb') as f:
                readData = base64.b64encode(f.read())
                return "Image Uploaded!", 200
        except:
            return "Error in processing image", 400
    else:
        return {"error":"Only JPG,PNG and JPEG is accepted"}, 400



if __name__=="__main__":
    app.run()