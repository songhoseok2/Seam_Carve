import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, static_folder="static")
app.config["UPLOAD_FOLDER"] = os.path.join(APP_ROOT, "static/uploaded_images").replace('\\', '/')
app.config["MAX_CONTENT_PATH"] = 500 * 1024 * 1024


@app.route('/')
def homepage():
    print("DEBUG: hello", flush=True)
    return render_template("upload.html")

@app.route('/about')
def about():
    return render_template("about.html", title="input_title")

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        upload_folder = app.config["UPLOAD_FOLDER"]
        if not os.path.isdir(upload_folder):
            print("DEBUG: making a new dir", flush=True)
            os.makedirs(upload_folder)
        target = app.config["UPLOAD_FOLDER"]
        uploaded_image = request.files["uploaded_image"]
        uploaded_image_name = secure_filename(uploaded_image.filename)
        destination = '/'.join([target, uploaded_image_name])
        uploaded_image.save(destination)
        print("DEBUG: target:", target, flush=True)
        print("DEBUG: filename:", uploaded_image.filename, flush=True)
        print("DEBUG: destination:", destination, flush=True)
        return render_template("upload_complete.html", uploaded_image_url="static/uploaded_images/" + uploaded_image.filename)
    else:
        return render_template("upload_complete.html")



if __name__ == "__main__":
    app.run(port=5000, debug=True)