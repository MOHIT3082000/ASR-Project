#!/usr/bin/env python3
"""
# Local Automatic Speech Recognition (ASR) System

A terminal-based ASR system using the open-source `faster-whisper` model that records
audio from the microphone and transcribes it locally without external APIs.

## Requirements Installation

```bash
pip install sounddevice scipy faster-whisper numpy torch
```

## Usage

Basic usage (records 60 seconds of audio by default):
```bash
python local_asr.py
```

Record for a specific duration:
```bash
python local_asr.py --duration 30
```

Use a specific whisper model size (options: tiny, base, small, medium, large):
```bash
python local_asr.py --model small
```

Check for and download the latest model:
```bash
python local_asr.py --download-latest
```

## Features
- Records audio from the microphone with configurable duration
- Saves the audio locally in .wav format
- Transcribes audio using faster-whisper with high accuracy
- Automatically uses GPU if available (fallback to CPU)
- Includes comprehensive error handling
- Provides CLI argument support for flexible recording time
"""

import os
import sys
import time
import argparse
import traceback
from datetime import datetime

# Audio processing libraries
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write as write_wav

# Import faster-whisper for transcription
try:
    from faster_whisper import WhisperModel, download_model
except ImportError:
    print("Error: faster-whisper is not installed. Please install it using:")
    print("pip install faster-whisper")
    sys.exit(1)

# Check if CUDA is available
def is_cuda_available():
    try:
        import torch
        return torch.cuda.is_available()
    except ImportError:
        print("PyTorch not installed. Will use CPU for inference.")
        return False

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Local ASR System with faster-whisper")
    parser.add_argument("--duration", type=int, default=60, 
                        help="Duration to record audio in seconds (default: 60)")
    parser.add_argument("--model", type=str, default="base", 
                        choices=["tiny", "base", "small", "medium", "large"],
                        help="Whisper model size to use (default: base)")
    parser.add_argument("--sample-rate", type=int, default=16000,
                        help="Audio sample rate in Hz (default: 16000)")
    parser.add_argument("--download-latest", action="store_true",
                        help="Check for and download the latest model")
    
    args = parser.parse_args()
    return args

def create_output_directory(base_dir="recordings"):
    """Create directory for storing recordings if it doesn't exist."""
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    return base_dir

def record_audio(duration, sample_rate):
    """
    Record audio from the microphone for the specified duration.
    
    Args:
        duration (int): Recording duration in seconds
        sample_rate (int): Audio sample rate in Hz
        
    Returns:
        np.ndarray: Recorded audio data
    """
    if duration <= 0:
        print("Error: Duration must be a positive integer.")
        sys.exit(1)

    print(f"Recording audio for {duration} seconds...")
    print("Speak now...")
    
    try:
        # Record audio
        audio_data = sd.rec(
            int(duration * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype=np.float32
        )
        
        # Display a countdown timer
        for remaining in range(duration, 0, -1):
            sys.stdout.write(f"\rRecording: {remaining} seconds remaining...")
            sys.stdout.flush()
            time.sleep(1)
            
        print("\nRecording complete.")
        
        # Wait for recording to complete
        sd.wait()
        
        return audio_data
    except Exception as e:
        print(f"Error recording audio: {e}")
        traceback.print_exc()
        sys.exit(1)

def save_audio(audio_data, sample_rate, output_dir):
    """
    Save the recorded audio to a WAV file.
    
    Args:
        audio_data (np.ndarray): Audio data to save
        sample_rate (int): Audio sample rate in Hz
        output_dir (str): Directory to save the audio file
        
    Returns:
        str: Path to the saved audio file
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(output_dir, f"recording_{timestamp}.wav")
    
    try:
        # Convert float32 to int16
        audio_int16 = (audio_data * 32767).astype(np.int16)
        
        # Save as WAV file
        write_wav(filename, sample_rate, audio_int16)
        print(f"Audio saved to: {filename}")
        return filename
    except Exception as e:
        print(f"Error saving audio file: {e}")
        traceback.print_exc()
        return None

def load_whisper_model(model_size, download_latest=False):
    """
    Load the faster-whisper model.
    
    Args:
        model_size (str): Size of the model to load (tiny, base, small, medium, large)
        download_latest (bool): Whether to check for and download the latest model
        
    Returns:
        WhisperModel: Loaded faster-whisper model
    """
    # Determine device
    if is_cuda_available():
        print(f"CUDA is available. Using GPU for inference.")
        device = "cuda"
        compute_type = "float16"  # For GPU
    else:
        print("CUDA is not available. Using CPU for inference.")
        device = "cpu"
        compute_type = "int8"  # For CPU
    
    try:
        if download_latest:
            print(f"Checking for latest {model_size} model and downloading if needed...")
            # Use faster-whisper's download_model function to download/update model
            download_model(model_size)
            print("Latest model downloaded or already up to date.")
        
        print(f"Loading {model_size} model...")
        model = WhisperModel(model_size, device=device, compute_type=compute_type)
        print(f"Model loaded successfully.")
        return model
    except Exception as e:
        print(f"Error loading Whisper model: {e}")
        traceback.print_exc()
        sys.exit(1)

def transcribe_audio(model, audio_file):
    """
    Transcribe audio using the faster-whisper model.
    
    Args:
        model (WhisperModel): Initialized faster-whisper model
        audio_file (str): Path to the audio file to transcribe
        
    Returns:
        str: Transcription result
    """
    try:
        print("Transcribing audio...")
        start_time = time.time()
        
        # Run transcription with high accuracy settings
        segments, info = model.transcribe(
            audio_file,
            beam_size=5,        # Increase beam size for better accuracy
            word_timestamps=True,
            vad_filter=True,    # Voice activity detection to filter out silence
            vad_parameters=dict(min_silence_duration_ms=500)
        )
        
        # Collect segments
        transcript = ""
        for segment in segments:
            transcript += segment.text + " "
        
        processing_time = time.time() - start_time
        print(f"Transcription completed in {processing_time:.2f} seconds.")
        
        return transcript.strip()
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        traceback.print_exc()
        return "Transcription failed. Please check logs."

def main():
    """Main function to run the ASR system."""
    try:
        # Parse command line arguments
        args = parse_arguments()
        
        # Create output directory
        output_dir = create_output_directory()
        
        # Load Whisper model
        model = load_whisper_model(args.model, args.download_latest)
        
        # Record audio
        audio_data = record_audio(args.duration, args.sample_rate)
        
        # Save audio to file
        audio_file = save_audio(audio_data, args.sample_rate, output_dir)
        if not audio_file:
            print("Failed to save audio file. Exiting.")
            sys.exit(1)
            
        # Transcribe audio
        transcript = transcribe_audio(model, audio_file)
        
        # Display results
        print("\n" + "="*50)
        print("TRANSCRIPTION RESULT:")
        print("="*50)
        print(transcript)
        print("="*50)
        
    except KeyboardInterrupt:
        print("\nProcess interrupted by user. Exiting.")
        sys.exit(0)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
