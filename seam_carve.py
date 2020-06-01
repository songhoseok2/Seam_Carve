import os
from flask import Flask, render_template, request, Response
from werkzeug.utils import secure_filename
from seam_carve_algorithm import seam_carve

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, static_folder="static")
app.config["UPLOAD_FOLDER"] = os.path.join(APP_ROOT, "static/uploaded_images").replace('\\', '/')
app.config["MAX_CONTENT_PATH"] = 500 * 1024 * 1024
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route('/')
def homepage():
    print("DEBUG: hello", flush=True)
    return render_template("upload.html")

@app.route('/process', methods=['GET', 'POST'])
def process():
    requested_img_name = request.form["img_name"]
    width_scale = request.form["width_scale"]
    height_scale = request.form["height_scale"]
    print("DEBUG: request:", request, flush=True)
    print("DEBUG: requested_img_name:", requested_img_name, flush=True)
    print("DEBUG: width_scale:", width_scale, flush=True)
    seam_carve(requested_img_name, height_scale, width_scale)

    return Response('', status=200, mimetype='application/json')


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
        return render_template("carving_page.html", uploaded_image_filename=uploaded_image.filename)
    else:
        return render_template("carving_page.html")



if __name__ == "__main__":
    app.run(port=5000, debug=True)