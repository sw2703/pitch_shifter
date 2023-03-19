# Pitch Shifter

This repository contains a simple Flask web application that allows users to upload a MIDI file and transpose the notes by a specified number of semitones. The app then returns the transformed MIDI file for download.

## Features

- Upload MIDI files
- Transpose notes by a user-specified number of semitones
- Download the transformed MIDI file

## Installation

1. Clone the repository:

```bash
git clone https://github.com/sw2703/pitch-shifter.git
cd pitch-shifter
```

2. Create a virtual environment and activate it:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Run the Flask application:

```bash
python app.py
```

2. Open your web browser and navigate to `http://127.0.0.1:5000/`.

3. Use the web interface to upload a MIDI file, specify the number of semitones to transpose, and download the transformed file.

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
