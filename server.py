from flask import Flask, render_template, request, redirect
import os
from werkzeug.utils import secure_filename
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from scipy.io import wavfile
import mutagen



UPLOAD_FOLDER = "C:\\Users\\DELL\\python preojects\\koolio project"
ALLOWED_EXTENSIONS = {'mp3', 'wav'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        f = request.files['file1']
        filename = f.filename
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename)))
        return redirect(f'/metadata/{filename}')
    return render_template("index.html")

@app.route("/metadata/<filename>")
def metadata(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if filename.rsplit('.', 1)[1].lower() == 'mp3':
        try:
            audio = EasyID3(filepath)
        except mutagen.id3.ID3NoHeaderError:
            audio = mutagen.File(filepath, easy=True)
            audio.add_tags()
        metadata = {'title': audio.get('title', [''])[0], 
                    'artist': audio.get('artist', ['']), 
                    'genre': audio.get('genre', [''])[0],
                    'size': os.path.getsize(filename),
                    'length': MP3(filename).info.length}
    elif filename.rsplit('.', 1)[1].lower() == 'wav':
        samplerate, data= wavfile.read(filepath)
        metadata = {
            'title': 'Not found',
            'artist': 'Not found',
            'genre': 'Not found',
            'size': data.size,
            'length': data.shape[0] / samplerate,

        }

    return render_template('metadata.html', metadata=metadata)


if __name__ == '__main__':
    app.run(debug=True)