# Project Summary Notes: Local Automatic Speech Recognition (ASR) System

## Project Overview
This project is a terminal-based Local Automatic Speech Recognition (ASR) system that uses the open-source `faster-whisper` model to record audio from a microphone and transcribe it locally without relying on external APIs. It is designed to be resource-efficient, privacy-focused, and developer-friendly.

## Key Components

### Audio Recording System
- Uses the `sounddevice` library with NumPy for audio capture.
- Records single-channel (mono) audio at a fixed 16kHz sample rate.
- Audio is recorded internally in float32 format and saved as int16 WAV files with timestamps.

### Whisper Model Integration
- Utilizes the `faster-whisper` library, which offers faster transcription with comparable accuracy to OpenAI's Whisper.
- Supports multiple model sizes (tiny, base, small, medium, large) with varying RAM and performance requirements.
- GPU acceleration uses float16 precision; CPU mode uses int8 quantization.
- Includes beam search and voice activity detection (VAD) for improved accuracy.

## Performance and System Requirements
- Requires Python 3.8 or higher.
- Minimum 8GB RAM recommended; GPU support optional but improves speed significantly.
- Base and small models recommended for 8GB RAM systems; medium and large models require more resources.

## Usage Summary
- Run `python local_asr.py` to record and transcribe audio (default 60 seconds).
- CLI options allow specifying recording duration, model size, and downloading the latest model.
- Audio recordings are saved locally in WAV format with timestamped filenames.

## Potential Extensions and Future Work
- Add confidence scores and word-level timestamps.
- Support continuous recording and speaker diarization.
- Develop a GUI interface and audio pre-processing features.
- Enable real-time streaming transcription and multi-language support.
- Integrate with note-taking applications and provide export options.

## Technical Considerations and Limitations
- Audio quality depends on microphone and environment.
- Smaller models trade accuracy for speed and lower memory usage.
- Current implementation is batch processing only; no real-time streaming.
- Error handling includes detailed logging and graceful exits.

## Summary
This project provides a robust, offline ASR solution suitable for educational, professional, and accessibility use cases. It balances performance and resource usage while maintaining privacy by avoiding external API calls.
