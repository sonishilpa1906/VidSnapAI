from flask import Flask, render_template, request
import uuid
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = "user_uploads"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/create", methods=["GET", "POST"])
def create():
    my_id = uuid.uuid1()
    if(request.method == "POST"):
       desc = request.form.get("text")
       filepath = os.path.join(app.config['UPLOAD_FOLDER'],str(my_id))
       if not (os.path.exists(filepath)):
            os.mkdir(filepath)
       with open(os.path.join(filepath,"desc.txt"),"w") as f:
          f.write(desc)

       input_files = []       
       for key, value in request.files.items():
            file = request.files[key]
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(filepath, filename))
                input_files.append(filename)

       for file in input_files:
            with open(os.path.join(filepath, "input.txt"),"a") as f:
                f.write(f"file '{file}'\nduration 1\n")

           

    return render_template("create.html", my_id = my_id)

@app.route("/gallery")
def gallery():
    reels = os.listdir("static/reels")
    return render_template("gallery.html", reels = reels)

app.run(debug=True)