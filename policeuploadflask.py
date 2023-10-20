from flask import Flask, request, render_template
import os
from werkzeug.utils import secure_filename
from s3upload import upload_S3


app = Flask(__name__,template_folder='templates')

# Specify the upload folder
UPLOAD_FOLDER = 'PoliceUploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


# Function to check if a file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('Police.html')


@app.route('/uploadedoffender', methods=['POST'])
def upload_file():
    print(request.files)
    # Check if a file was submitted
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']

    # If the user does not select a file, the browser submits an empty file without a filename
    if file.filename == '':
        return 'No selected file'

    # Check if the file has an allowed extension
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        #The below code first uploads the uploaded image locally onto the system and then calls the function make_binary that makes sure that the image is converted into b
        #binary format and then it returns the binary image onto temp. Now with create_response(temp) the response is created
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        val = request.form.get("inputvalue")
        print(val)
        path = "PoliceUploads/"+filename
        upload_S3(filename,val)
        return "done"

if __name__ == "__main__":
    app.run(port=2223,debug=True)
