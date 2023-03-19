from flask import Flask, request, send_from_directory
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Save the uploaded file
        file = request.files["file"]
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Get the semitones value from the form
        semitones = int(request.form.get('semitones', -2))

        # Process the file with your Python script
        output_filepath = process_file(filepath, semitones)

        # Send the processed file for download
        return send_from_directory(directory=os.path.dirname(output_filepath),
                                   path=os.path.basename(output_filepath),
                                   as_attachment=True)
    return '''
    <!doctype html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>File Transformer</title>
        <style>
            #drop-area {
                border: 2px dashed #ccc;
                border-radius: 20px;
                width: 480px;
                height: 200px;
                padding: 20px;
                display: flex;
                align-items: center;
                justify-content: center;
                margin: 50px auto;
            }
            #drop-area.highlight {
                border-color: #f00;
            }
        </style>
    </head>
    <body>
        <form id="upload-form" method="POST" enctype="multipart/form-data">
            <label for="semitones">Semitones:</label>
            <input type="number" id="semitones" name="semitones" value="-2"><br><br>
            <div id="drop-area">
                <input type="file" id="fileElem" name="file" style="display:none">
                <label for="fileElem">Drag & drop a file here or click to select</label>
            </div>
        </form>
        <script>
            const dropArea = document.getElementById("drop-area");
            const form = document.getElementById("upload-form");
            const fileInput = document.getElementById("fileElem");

            ["dragenter", "dragover", "dragleave", "drop"].forEach(eventName => {
                dropArea.addEventListener(eventName, preventDefaults, false);
            });

            function preventDefaults(e) {
                e.preventDefault();
                e.stopPropagation();
            }

            ["dragenter", "dragover"].forEach(eventName => {
                dropArea.addEventListener(eventName, highlight, false);
            });

            ["dragleave", "drop"].forEach(eventName => {
                dropArea.addEventListener(eventName, unhighlight, false);
            });

            function highlight(e) {
                dropArea.classList.add("highlight");
            }

            function unhighlight(e) {
                dropArea.classList.remove("highlight");
            }

            dropArea.addEventListener("drop", handleDrop, false);

            function handleDrop(e) {
                const dt = e.dataTransfer;
                const file = dt.files[0];
                fileInput.files = dt.files;
                form.submit();
            }
        </script>
    </body>
    </html>
    '''

import mido
from mido import MidiFile, MidiTrack, Message

def process_file(filepath, semitones):
    original_midi = MidiFile(filepath)
    transposed_midi = MidiFile()
    output_filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"transformed_{os.path.basename(filepath)}")

    for track in original_midi.tracks:
        new_track = MidiTrack()
        transposed_midi.tracks.append(new_track)

        for msg in track:
            if msg.type == 'note_on' or msg.type == 'note_off':
                new_note = msg.note + semitones
                new_note = max(0, min(127, new_note))  # Ensure note is within valid range
                new_msg = Message(msg.type, channel=msg.channel, note=new_note, velocity=msg.velocity, time=msg.time)
                new_track.append(new_msg)
            else:
                new_track.append(msg)

    transposed_midi.save(output_filepath)
    return output_filepath

if __name__ == "__main__":
    app.run(debug=True)   
