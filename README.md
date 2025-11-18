# Music Sprint

> An idle runner where every song creates a unique level. Your character automatically dodges obstacles generated from music beats, frequencies, and amplitudes in real-time.

## Project Status: Phase 1 (Prototype)

Current milestone: Audio analysis and waveform processing prototype

## What is Music Sprint?

Music Sprint is a music-driven idle runner game where:
- Your music library becomes the game content
- Audio waveforms are analyzed in real-time to generate unique courses
- Characters automatically run and dodge obstacles synced to the music
- Every song creates a completely different gameplay experience

### Key Features (Planned)

- **Automatic Course Generation**: Beat detection, frequency analysis, and amplitude tracking create dynamic obstacles
- **Idle Gameplay**: Characters auto-run and auto-dodge to the rhythm
- **Music Platform Integration**: Spotify, local files (.mp3, .wav, .flac)
- **Social Competition**: Compete on the same track with other players
- **Difficulty Scaling**: Course complexity adapts to song characteristics

## Phase 1: Audio Analysis Prototype

### Completed Features

- AudioLoader class: Load and validate audio files (.mp3, .wav, .flac, .ogg)
- AudioAnalyzer class: Extract game-relevant features from audio
  - FFT (Fast Fourier Transform) analysis
  - Beat detection
  - Amplitude envelope extraction
  - Spectral features (centroid, rolloff, zero-crossing rate)
  - Automatic difficulty calculation
- File selection UI (tkinter-based)
- Command-line demo application

### Project Structure

```
music_sprint/
├── src/
│   ├── audio/
│   │   ├── audio_loader.py    # Audio file loading
│   │   └── audio_analyzer.py  # Waveform analysis
│   ├── ui/
│   │   └── file_dialog.py     # File selection UI
│   └── main.py                # Demo application
├── tests/
│   └── test_audio.py          # Unit & integration tests
├── assets/
│   └── sample_music/          # Sample audio files
└── requirements.txt
```

## Installation

### Prerequisites

- Python 3.8+
- pip

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/VC-MusicSprint.git
cd VC-MusicSprint

# Install dependencies
pip install -r requirements.txt
```

### Dependencies

- `librosa`: Audio analysis and feature extraction
- `numpy`: Numerical computing
- `soundfile`: Audio file I/O
- `pygame`: Game engine (for future phases)
- `pytest`: Testing framework

## Usage (Phase 1)

### Run the demo

```bash
python src/main.py
```

This will:
1. Open a file dialog to select an audio file
2. Load and analyze the audio
3. Display extracted features (beats, tempo, difficulty, etc.)
4. Optionally save analysis results as JSON

### Run tests

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_audio.py

# Run with verbose output
pytest -v
```

## Architecture (OOP Design)

This project strictly follows Object-Oriented Programming principles:

### Design Principles

- **Encapsulation**: Internal data (waveforms, features) are private
- **Single Responsibility**: Each class has one clear purpose
  - `AudioLoader`: File loading only
  - `AudioAnalyzer`: Waveform analysis only
  - `FileDialog`: UI interaction only
- **Separation of Concerns**: Audio processing, UI, and game logic are isolated

### SOLID Compliance

- **S**ingle Responsibility: Each class has one job
- **O**pen/Closed: Extensible for new music platforms without modifying existing code
- **L**iskov Substitution: (Future) All `MusicProvider` implementations are interchangeable
- **I**nterface Segregation: Minimal, focused interfaces
- **D**ependency Inversion: High-level modules depend on abstractions

## Roadmap

### Phase 1: Prototype (Current - Week 1-1.5)
- [x] Project structure
- [x] AudioLoader class
- [x] AudioAnalyzer class (FFT, beat detection, amplitude)
- [x] Basic UI (file dialog)
- [ ] Test with 3 sample songs

### Phase 2: Course Generation (Week 2.5-4)
- [ ] CourseGenerator class (Factory pattern)
- [ ] Obstacle class hierarchy (inheritance)
- [ ] Beat → Obstacle mapping algorithm
- [ ] Course visualization

### Phase 3: Character & Auto-Play (Week 4.5-6.5)
- [ ] Character class with auto-jump/duck
- [ ] AutoPlayController (Strategy pattern)
- [ ] Game main loop with music synchronization
- [ ] PyGame rendering

### Phase 4: Game Loop & Scoring (Week 7-8.5)
- [ ] ScoreManager class
- [ ] Combo system
- [ ] Local high scores
- [ ] Result screen with stats

### Phase 5: Polish & MVP Release (Week 9-10)
- [ ] UI/UX improvements
- [ ] Performance optimization
- [ ] Bug fixes
- [ ] README and documentation
- [ ] GitHub release

## Development Philosophy

- **1-person developer optimized**: Realistic timelines and scope
- **Iterative development**: Working prototype every phase
- **Code quality over speed**: Clean, maintainable OOP code
- **Portfolio-ready**: Professional-grade architecture and documentation

## License

See [LICENSE](LICENSE) file for details.

## Contributing

This is currently a solo project for portfolio purposes. Feedback and suggestions are welcome via Issues.

## Contact

Project maintained by: [Your Name]
- GitHub: [@yourusername](https://github.com/yourusername)
