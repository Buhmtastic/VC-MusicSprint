# Music Sprint

> An idle runner where every song creates a unique level. Your character automatically dodges obstacles generated from music beats, frequencies, and amplitudes in real-time.

## Project Status: Phase 3 Completed

**Current milestone**: Character & Auto-Play System ✅
**Completed**: Phase 1 (Audio Analysis) + Phase 2 (Course Generation) + Phase 3 (Character & Auto-Play)
**Next**: Phase 4 (Scoring & Results)

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

## Completed Phases

### Phase 1: Audio Analysis Prototype ✅

**Completed Features:**
- AudioLoader class: Load and validate audio files (.mp3, .wav, .flac, .ogg)
- AudioAnalyzer class: Extract game-relevant features from audio
  - FFT (Fast Fourier Transform) analysis
  - Beat detection
  - Amplitude envelope extraction
  - Spectral features (centroid, rolloff, zero-crossing rate)
  - Automatic difficulty calculation
- File selection UI (tkinter-based)
- Command-line demo application

### Phase 2: Course Generation System ✅

**Completed Features:**
- **Obstacle Class Hierarchy** (Inheritance & Polymorphism)
  - `Obstacle` (Abstract Base Class): Common interface for all obstacles
  - `BeatObstacle`: Beat-based obstacles (red, synced to rhythm)
  - `FrequencyWall`: Frequency-based walls (blue, height varies with pitch)
  - `AmplitudeGap`: Volume-based gaps (green, width varies with loudness)

- **Course Class**: Course management and timeline
  - Add/manage obstacles with time-based indexing
  - Query obstacles by time range
  - Statistics and metadata tracking

- **CourseGenerator** (Factory Pattern)
  - Convert audio features → Course objects
  - Mapping algorithms:
    - Beat → BeatObstacle (80% spawn probability)
    - Frequency → FrequencyWall (0.5s sampling)
    - Amplitude → AmplitudeGap (1.0s sampling, filtered by threshold)

- **CourseVisualizer**: matplotlib-based visualization
  - Color-coded obstacle rendering
  - Statistics overlay
  - PNG export and multi-course comparison

### Phase 3: Character & Auto-Play System ✅

**Completed Features:**
- **Character Class** (OOP Encapsulation)
  - Private attributes (_x, _y, _velocity_y) with property accessors
  - Physics simulation (gravity, jumping, landing)
  - State management (RUNNING, JUMPING, DUCKING)
  - Auto-jump and auto-duck methods

- **AutoPlayController** (Strategy Pattern)
  - AI decision-making system
  - Obstacle-specific avoidance strategies:
    - BeatObstacle → Jump
    - FrequencyWall → Jump (mid) or Duck (high)
    - AmplitudeGap → Jump (large gaps)
  - Reaction time simulation (150ms)
  - Difficulty scaling (0.0~2.0)

- **Game Class** (Main Game Loop)
  - Music synchronization (±50ms accuracy)
  - Active obstacle management (±2s window)
  - AABB collision detection
  - Score calculation system
  - Game state management (NOT_STARTED, PLAYING, PAUSED, FINISHED)

- **GameRenderer** (PyGame Rendering)
  - Character animations (running, jumping, ducking)
  - Real-time waveform background
  - Obstacle rendering with color coding
  - UI elements (score, time, progress)
  - 60 FPS stable rendering

- **Test Suite**: 29 unit tests (100% pass rate)
- **Demo Application**: Interactive PyGame demo with auto-play

### Project Structure

```
music_sprint/
├── src/
│   ├── audio/
│   │   ├── audio_loader.py        # Audio file loading
│   │   └── audio_analyzer.py      # Waveform analysis
│   ├── course/                     # Phase 2
│   │   ├── obstacle.py            # Obstacle hierarchy (ABC)
│   │   ├── course.py              # Course management
│   │   ├── course_generator.py   # Factory pattern
│   │   └── visualizer.py          # Visualization
│   ├── game/                       # ✨ Phase 3
│   │   ├── character.py           # Character physics & state
│   │   ├── auto_play_controller.py # AI decision-making
│   │   ├── game.py                # Main game loop
│   │   └── renderer.py            # PyGame rendering
│   ├── ui/
│   │   └── file_dialog.py         # File selection UI
│   └── main.py                    # Phase 1 demo
├── tests/
│   ├── test_audio.py              # Phase 1 tests
│   ├── test_course.py             # Phase 2 tests
│   └── test_game.py               # ✨ Phase 3 tests
├── demo_phase2.py                 # Phase 2 demo
├── demo_phase3.py                 # ✨ Phase 3 demo
├── assets/
│   └── sample_music/              # Sample audio files
├── 20251118_DevLog_MS01.md        # Phase 1 dev log
├── 20251118_DevLog_MS02.md        # Phase 2 dev log
├── 20251118_DevLog_MS03.md        # ✨ Phase 3 dev log
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

- `librosa >= 0.10.0`: Audio analysis and feature extraction
- `numpy >= 1.24.0`: Numerical computing
- `soundfile >= 0.12.0`: Audio file I/O
- `matplotlib >= 3.7.0`: Course visualization (Phase 2+)
- `pygame >= 2.5.0`: Game engine (Phase 3+)
- `pytest >= 7.4.0`: Testing framework

## Usage

### Phase 1 Demo: Audio Analysis

```bash
python src/main.py
```

This will:
1. Open a file dialog to select an audio file
2. Load and analyze the audio
3. Display extracted features (beats, tempo, difficulty, etc.)
4. Optionally save analysis results as JSON

### Phase 2 Demo: Course Generation

```bash
python demo_phase2.py
```

This will:
1. Generate a dummy audio waveform (5s, 440Hz)
2. Analyze the audio with AudioAnalyzer
3. Generate a course with CourseGenerator
4. Display obstacle statistics
5. Save course visualization to `assets/phase2_demo_course.png`

### Phase 3 Demo: Character & Auto-Play

```bash
python demo_phase3.py
```

This will:
1. Generate test audio (10s with beat pattern)
2. Analyze audio and generate course
3. Launch PyGame window with auto-play demonstration
4. Show character automatically dodging obstacles
5. Display real-time score and statistics

**Controls:**
- SPACE: Start game
- ESC: Exit

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

This project strictly follows Object-Oriented Programming principles with advanced design patterns:

### Design Patterns Implemented

**Phase 1:**
- **Encapsulation**: Internal data (waveforms, features) are private
- **Single Responsibility**: Each class has one clear purpose
  - `AudioLoader`: File loading only
  - `AudioAnalyzer`: Waveform analysis only
  - `FileDialog`: UI interaction only

**Phase 2:**
- **Inheritance**: `Obstacle` ABC with 3 concrete implementations
  ```
  Obstacle (ABC)
  ├── BeatObstacle
  ├── FrequencyWall
  └── AmplitudeGap
  ```
- **Polymorphism**: All obstacles share common interface (`get_height()`, `get_color()`, etc.)
- **Factory Pattern**: `CourseGenerator.generate()` creates Course objects
- **Abstract Base Classes**: Python's ABC module for enforcing interfaces

**Phase 3:**
- **Strategy Pattern**: `AutoPlayController` selects different strategies per obstacle type
  - `_strategy_for_beat()`: Jump strategy
  - `_strategy_for_frequency()`: Duck or jump based on height
  - `_strategy_for_amplitude()`: Jump for large gaps
- **Encapsulation**: Character internal state (`_x`, `_y`, `_velocity_y`) with property accessors
- **Dependency Injection**: Game receives Course and waveform externally
- **State Pattern**: Character states (RUNNING, JUMPING, DUCKING)

### SOLID Compliance

- **S**ingle Responsibility: Each class has one job
  - `Course`: Obstacle management only
  - `CourseGenerator`: Course creation only
  - `CourseVisualizer`: Visualization only
  - `Character`: Physics and state only
  - `AutoPlayController`: Decision-making only
  - `Game`: Game loop coordination only
  - `GameRenderer`: Rendering only
- **O**pen/Closed: Extensible for new obstacle types without modifying existing code
- **L**iskov Substitution: All `Obstacle` subclasses are interchangeable
- **I**nterface Segregation: Minimal, focused interfaces
- **D**ependency Inversion: High-level modules depend on abstractions (Obstacle ABC)

## Roadmap

### Phase 1: Prototype ✅ COMPLETED
- [x] Project structure
- [x] AudioLoader class
- [x] AudioAnalyzer class (FFT, beat detection, amplitude)
- [x] Basic UI (file dialog)
- [x] Unit tests and integration tests
- [x] DevLog (20251118_DevLog_MS01.md)

### Phase 2: Course Generation ✅ COMPLETED
- [x] CourseGenerator class (Factory pattern)
- [x] Obstacle class hierarchy (inheritance & polymorphism)
  - [x] Obstacle (Abstract Base Class)
  - [x] BeatObstacle, FrequencyWall, AmplitudeGap
- [x] Beat → Obstacle mapping algorithm
- [x] Frequency → Height mapping algorithm
- [x] Amplitude → Gap mapping algorithm
- [x] Course class (timeline management)
- [x] Course visualization (matplotlib)
- [x] Unit tests and integration tests
- [x] DevLog (20251118_DevLog_MS02.md)

### Phase 3: Character & Auto-Play ✅ COMPLETED
- [x] Character class with auto-jump/duck
- [x] AutoPlayController (Strategy pattern)
- [x] Game main loop with music synchronization
- [x] Collision detection (AABB)
- [x] PyGame rendering
- [x] Character animations (running, jumping, ducking)
- [x] Waveform background rendering
- [x] Unit tests (29 tests - 100% pass)
- [x] DevLog (20251118_DevLog_MS03.md)

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
