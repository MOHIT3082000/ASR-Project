# Local Automatic Speech Recognition (ASR) System

This terminal-based ASR system uses the open-source `faster-whisper` model to record audio from your microphone and transcribe it locally without any external APIs.

## Features

- Records audio from the microphone with configurable duration
- Saves the audio locally in .wav format
- Transcribes audio using faster-whisper with high accuracy
- Automatically uses GPU if available (fallback to CPU)
- Provides CLI argument support for flexible recording time
- Works efficiently on machines with 8GB RAM

## Installation

### Windows
Run the `setup.bat` file or install dependencies manually:
```
pip install -r requirements.txt
```

### macOS/Linux
Run the `setup.sh` file or install dependencies manually:
```
pip install -r requirements.txt
```

## Usage

### Basic Usage
Record for 60 seconds (default):
```
python local_asr.py
```

### Record for a specific duration
```
python local_asr.py --duration 30
```

### Use a specific model size
Options: tiny, base, small, medium, large
```
python local_asr.py --model small
```

### Check for and download the latest model
```
python local_asr.py --download-latest
```

## Technical Details

- Using `sounddevice` and `scipy` for audio recording and saving
- Transcription powered by the `faster-whisper` library
- Automatic CPU/GPU detection using PyTorch
- Audio is saved in WAV format with a timestamp in the filename
- All processing is done locally with no external API calls

## System Requirements

- Python 3.8 or higher
- 8GB RAM (minimum)
- GPU support is optional but recommended for faster processing
