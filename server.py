from flask import Flask, render_template, redirect, url_for
from requests import request
import os
from mutagen.easyid3 import EasyID3

UPLOAD_FOLDER = 'C:/Users/DELL/python preojects/koolio project'
ALLOWED_EXTENSIONS = {'mp3'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files['file']
    filename = file.filename
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return redirect(url_for('metadata', filename=filename))

@app.route("/metadata/<filename>", methods=["POST"])
def metadata(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    audio = EasyID3(filepath)
    metadata = {'title': audio.get('title', [''])[0], 'artist': audio.get('artist', [''])[0]}
    return render_template('metadata.html', metadata=metadata)


if __name__ == '__main__':
    app.run(debug=True)