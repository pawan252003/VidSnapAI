from flask import Flask, render_template, request, redirect, url_for
import uuid
from werkzeug.utils import secure_filename
import os
from concurrent.futures import ThreadPoolExecutor
from generate_process import process_folder
import sys
from PIL import Image

#this is to noramlize any imahe ext.
def normalize_image(path):
    with Image.open(path) as img:
        rgb = img.convert("RGB")
        rgb.save(path, "JPEG")

# this is for charachter encoding
sys.stdout.reconfigure(encoding='utf-8')

executor = ThreadPoolExecutor(max_workers=2)
def safe_process(folder):
    try:
        process_folder(folder)
    except Exception as e:
        print("THREAD ERROR:", e)


UPLOAD_FOLDER = 'user_uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    reels_dir = os.path.join("static", "reels")
    featured_reels = []

    if os.path.exists(reels_dir):
        reels = [
            f for f in os.listdir(reels_dir)
            if f.endswith(".mp4")
        ]

        # sort newest first
        reels.sort(
            key=lambda x: os.path.getmtime(os.path.join(reels_dir, x)),
            reverse=True
        )

        featured_reels = reels[:5]  # top 5 featured

    return render_template("home.html", featured_reels=featured_reels)


@app.route("/create", methods=["GET", "POST"])
def create():
    myid = str(uuid.uuid1())
    if request.method == "POST":
        res_id = request.form.get('uuid')
        desc = request.form.get('text')

        input_files = []

        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], res_id)
        os.makedirs(upload_path, exist_ok=True)

        # Save uploaded files
        for key, file in request.files.items():
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(upload_path, filename))
                normalize_image(os.path.join(upload_path, filename))
                input_files.append(filename)

        if not input_files:
            return "No valid files uploaded", 400

        # Save description
        with open(os.path.join(upload_path, 'desc.txt'), 'w') as f:
            f.write(desc)

        # Create input.txt with full paths for ffmpeg
        input_txt_path = os.path.join(upload_path, "input.txt")
        with open(input_txt_path, "w") as f:
            for fl in input_files:
                full_path = os.path.abspath(os.path.join(upload_path, fl))
                f.write(f"file '{full_path}'\n")
                f.write("duration 2\n")
            #repeat last image WITHOUT duration
            last_path = os.path.abspath(os.path.join(upload_path, input_files[-1]))
            f.write(f"file '{last_path}'\n")

        # Submit folder for background processing
        executor.submit(safe_process, res_id)

        return redirect(url_for("gallery"))

    return render_template("create.html", myid=myid)

@app.route("/gallery")
def gallery():
    reels_dir = os.path.join("static", "reels")
    os.makedirs(reels_dir, exist_ok=True)
    reels = [f for f in os.listdir(reels_dir) if f.endswith(".mp4")]
    return render_template("gallery.html", reels=reels)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000)) 
    app.run(host="0.0.0.0", port=port)

