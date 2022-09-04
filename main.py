from msilib.schema import File
from flask import Flask, request, Response
from werkzeug.utils import secure_filename
import os
from SuperResolution import SuperResolution
import io, base64
from PIL import Image

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


@app.route("/images", methods=["GET"])
def getAllImages():
    temp = os.listdir('./static/output_images')
    images = []
    for image in temp:
        images.append("/static/output_images/"+image)
    return images, 200

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
                return readData, 200

        except:
            return "Error in processing image", 400
    else:
        return {"error":"Only JPG,PNG and JPEG is accepted"}, 400


@app.route("/enhance", methods=["POST"])
def Enhance():
    body = request.json
    print(body)
    if 'image' not in body and 'file_name' not in body and 'file_extension' not in body and body['file_extension'] not in ALLOWED_EXTENSIONS:
        return "Error Request", 400
    imageBase = body['image']
    imageName = body['file_name']
    extension = body['file_extension']
    try:
        fileName = imageName+"."+extension
        img = Image.open(io.BytesIO(base64.decodebytes(bytes(imageBase, "utf-8"))))
        inputPath = "./static/input_images/"+imageName+"."+extension
        img.save(inputPath)
        sr = SuperResolution()
        sr.predict(inputPath, fileName)
        with open("./static/output_images/enhanced_"+fileName, 'rb') as f:
            readData = base64.b64encode(f.read())
            return readData, 200
    except:
        return "Error in processing image", 400



if __name__=="__main__":
    app.run(host="192.168.245.32")