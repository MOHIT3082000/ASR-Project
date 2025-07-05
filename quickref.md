# ASR Usage Quick Reference

## Getting Started

### Installation
```bash
# Windows
setup.bat

# macOS/Linux
./setup.sh
```

### Basic Usage
```bash
# Record 60 seconds (default)
python local_asr.py

# Record 30 seconds
python local_asr.py --duration 30

# Use small model (better accuracy)
python local_asr.py --model small
```

## Command Options

| Option | Description | Default | Values |
|--------|-------------|---------|--------|
| `--duration` | Recording time in seconds | 60 | Any integer |
| `--model` | Whisper model size | base | tiny, base, small, medium, large |
| `--sample-rate` | Audio sample rate | 16000 | 16000, 44100, 48000 |
| `--download-latest` | Check for model updates | - | Flag (no value) |

## Hardware Requirements

| Model | Min RAM | Recommended RAM | GPU Recommended? |
|-------|---------|----------------|------------------|
| tiny  | 2GB     | 4GB            | No               |
| base  | 4GB     | 8GB            | No               |
| small | 6GB     | 8GB            | For speed        |
| medium| 8GB     | 16GB           | Yes              |
| large | 16GB    | 32GB           | Yes              |

## Accuracy Guidelines

| Condition | Recommended Model |
|-----------|------------------|
| Clear speech, quiet room | base |
| Normal conversation | small |
| Multiple speakers | medium |
| Technical terminology | medium/large |
| Non-English speech | medium/large |

## Troubleshooting

### Common Issues

**No audio recording:**
- Check microphone permissions
- Verify microphone is not muted
- Run `python -m sounddevice` to see available devices

**Out of memory:**
- Use smaller model
- Close other applications
- Add swap space/virtual memory

**Poor transcription quality:**
- Use larger model
- Improve microphone placement
- Reduce background noise
- Speak clearly and at moderate pace

**GPU not detected:**
- Install/update GPU drivers
- Verify PyTorch CUDA installation
- Run `python -c "import torch; print(torch.cuda.is_available())"` 

## Tips for Best Results

1. Use a quality microphone if possible
2. Record in a quiet environment
3. Speak clearly at a normal pace
4. Position microphone 6-12 inches from mouth
5. Try different model sizes to find accuracy/speed balance
6. For important recordings, use the small or medium model

## Recording Output

All recordings are saved in the `recordings` folder with timestamp-based filenames:
```
recordings/recording_YYYYMMDD_HHMMSS.wav
```

## Project Structure

```
recorded_asr/
├── local_asr.py       # Main script
├── requirements.txt   # Dependencies
├── setup.bat          # Windows setup
├── setup.sh           # Unix setup
├── README.md          # Documentation
├── project_notes.md   # Development notes
├── technical_guide.md # Technical details
└── recordings/        # Saved audio files
```
