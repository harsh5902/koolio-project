# koolio-project

This project is a simple web application that allows users to upload audio files, extracts metadata from them, and stores the metadata in a database. It uses the Flask web framework and SQLAlchemy.

## Features
Upload audio files (currently supports .mp3 and .wav files)
<br>
Read metadata from the uploaded audio files (file name, title, artist, genre, length, and file size)
<br>
Save the metadata to a SQLite database
<br>
View a list of all uploaded audio files and their metadata
<br>

## Usage
Open the web application in your browser on your localhost.
<br>
Click on the "Upload File" button and select an audio file to upload.
<br>
Once the file is uploaded, the metadata (title, artist, genre, length, and file size) will be displayed.
<br>
The metadata will also be saved to the database.
<br>
If the file is already in the database, an error message will be displayed.
<br>

## Credits
This project was created by Harsh Pande. It uses the following open source packages:
<br>
Flask
<br>
SQLAlchemy
<br>
Mutagen
<br>
Pydub
<br>
WTForms
<br>


Database:
![image](https://user-images.githubusercontent.com/74867899/236321748-e0f88cb3-3a3a-4d05-9190-88e6516c76a3.png)

Website:
![image](https://user-images.githubusercontent.com/74867899/236321933-66536b95-07d4-49f3-aff6-ad6d12e67ed3.png)
![image](https://user-images.githubusercontent.com/74867899/236322231-982701aa-b30c-4e1e-a7da-65265192451c.png)

