from flask import Flask, render_template, request, redirect
import os
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from scipy.io import wavfile
import mutagen



UPLOAD_FOLDER = "C:\\Users\\DELL\\python preojects\\koolio project"
ALLOWED_EXTENSIONS = {'mp3', 'wav'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///metadata.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class AudioFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255))
    artist = db.Column(db.String(255))
    genre = db.Column(db.String(255))
    length = db.Column(db.String(225))
    filesize = db.Column(db.String(225))

with app.app_context():
    db.create_all()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        f = request.files['file1']
        filename = f.filename
        f.save(os.path.join(f"{app.config['UPLOAD_FOLDER']}", secure_filename(filename)))
        return redirect(f'/metadata/{filename}')
    return render_template("index.html")

@app.route("/metadata/<filename>")
def metadata(filename):
    filepath = os.path.join(f"{app.config['UPLOAD_FOLDER']}", filename)
    if filename.rsplit('.', 1)[1].lower() == 'mp3':
        try:
            audio = EasyID3(filepath)
        except mutagen.id3.ID3NoHeaderError:
            audio = mutagen.File(filepath, easy=True)
            audio.add_tags()
        metadata = {'title': audio.get('title', ['NA'])[0], 
                    'artist': audio.get('artist', ['NA'])[0], 
                    'genre': audio.get('genre', ['NA'])[0],
                    'size': os.path.getsize(filename),
                    'length': MP3(filename).info.length}
        audio_file = AudioFile(
            filename=filename,
            artist=metadata['artist'],
            title=metadata['title'],
            genre=metadata['genre'],
            length=metadata['length'],
            filesize=metadata['size']
        )
        db.session.add(audio_file)
        db.session.commit()

    elif filename.rsplit('.', 1)[1].lower() == 'wav':
        samplerate, data= wavfile.read(filepath)
        metadata = {
            'title': 'NA',
            'artist': 'NA',
            'genre': 'NA',
            'size': data.size,
            'length': data.shape[0] / samplerate,
        }
        audio_file = AudioFile(
            filename=filename,
            artist=metadata['artist'],
            title=metadata['title'],
            genre=metadata['genre'],
            length=metadata['length'],
            filesize=metadata['size']
        )
        db.session.add(audio_file)
        db.session.commit()

    else:
        return "File format not supported"

    return render_template('metadata.html', metadata=metadata)

if __name__ == '__main__':
    app.run(debug=True)
