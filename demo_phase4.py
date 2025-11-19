# -*- coding: utf-8 -*-
"""
Phase 4 Demo Script
Scoring & Statistics System Test

실행 방법:
python demo_phase4.py
"""

import sys
from pathlib import Path
import numpy as np

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from src.audio.audio_analyzer import AudioAnalyzer
from src.course.course_generator import CourseGenerator
from src.score.score_manager import ScoreManager
from src.score.statistics_tracker import StatisticsTracker
from src.score.difficulty_analyzer import DifficultyAnalyzer


def main():
    """Phase 4 Demo 실행"""
    print("\n" + "="*70)
    print("  Music Sprint - Phase 4 Demo")
    print("  Scoring & Statistics System Test")
    print("="*70 + "\n")

    # 1. Generate test audio
    print("[1] Generating test audio...")
    duration = 10.0
    sample_rate = 22050
    t = np.linspace(0, duration, int(sample_rate * duration))

    # 비트감 있는 오디오
    base_freq = 440.0
    waveform = np.sin(2 * np.pi * base_freq * t)
    beat_envelope = 0.5 + 0.5 * np.sin(2 * np.pi * 2 * t)  # 2 Hz beats
    waveform = waveform * beat_envelope

    print(f"   [OK] Generated: {duration}s audio")

    # 2. Analyze audio
    print("\n[2] Analyzing audio...")
    analyzer = AudioAnalyzer()
    features = analyzer.analyze(waveform, sample_rate)

    print(f"   [OK] Analysis complete:")
    print(f"      - BPM: {features['tempo']['bpm']:.1f}")
    print(f"      - Beats: {features['beats']['count']}")
    print(f"      - Duration: {features['duration']:.2f}s")

    # 3. Generate course
    print("\n[3] Generating course...")
    generator = CourseGenerator(seed=42)
    course = generator.generate(features, course_name="Phase 4 Demo Course")

    stats = course.get_statistics()
    print(f"   [OK] Course generated:")
    print(f"      - Total obstacles: {stats['total_obstacles']}")
    print(f"      - Density: {stats['density']:.2f} obstacles/s")

    # 4. Analyze difficulty
    print("\n[4] Analyzing difficulty...")
    difficulty_analyzer = DifficultyAnalyzer()

    # From audio features
    diff_audio = difficulty_analyzer.analyze_difficulty(features)
    print(f"   [OK] Difficulty from audio:")
    print(f"      - Score: {diff_audio['difficulty_score']:.1f}/100")
    print(f"      - Level: {diff_audio['difficulty_level'].upper()}")

    # From course
    diff_course = difficulty_analyzer.analyze_difficulty_from_course(course)
    print(f"   [OK] Difficulty from course:")
    print(f"      - Score: {diff_course['difficulty_score']:.1f}/100")
    print(f"      - Level: {diff_course['difficulty_level'].upper()}")
    desc = difficulty_analyzer.get_difficulty_description(diff_course['difficulty_level'])
    print(f"      - Description: {desc}")

    # 5. Simulate game play
    print("\n[5] Simulating game play...")
    tracker = StatisticsTracker()

    # 장애물 회피 시뮬레이션
    total_obstacles = stats['total_obstacles']
    avoided = int(total_obstacles * 0.85)  # 85% 성공률
    hit = total_obstacles - avoided

    for i in range(avoided):
        is_perfect = (i % 3 == 0)  # 매 3번째는 perfect
        tracker.track_obstacle_avoided()
        if i % 2 == 0:
            tracker.track_jump(is_perfect=is_perfect, timing_accuracy=0.9 if is_perfect else 0.7)
        else:
            tracker.track_duck(is_perfect=is_perfect, timing_accuracy=0.85 if is_perfect else 0.65)

    for _ in range(hit):
        tracker.track_obstacle_hit()

    tracker.update_game_duration(duration)

    play_stats = tracker.get_summary()
    print(f"   [OK] Game simulation complete:")
    print(f"      - Obstacles avoided: {play_stats['obstacles_avoided']}")
    print(f"      - Obstacles hit: {play_stats['obstacles_hit']}")
    print(f"      - Success rate: {play_stats['success_rate']:.1f}%")
    print(f"      - Max combo: {play_stats['max_combo']}")
    print(f"      - Timing accuracy: {play_stats['timing_accuracy']:.2f}")

    # 6. Calculate score
    print("\n[6] Calculating final score...")
    score_manager = ScoreManager()

    score_info = score_manager.calculate_final_score(
        obstacles_avoided=play_stats['obstacles_avoided'],
        perfect_dodges=play_stats['total_perfect_actions'],
        max_combo=play_stats['max_combo'],
        accuracy=play_stats['timing_accuracy'],
        difficulty_level=diff_course['difficulty_level']
    )

    print(f"   [OK] Score calculation:")
    print(f"      - Base score: {score_info['base_score']}")
    print(f"      - Difficulty multiplier: {score_info['difficulty_multiplier']:.1f}x")
    print(f"      - FINAL SCORE: {score_info['final_score']}")

    # 7. Save high score
    print("\n[7] Saving high score...")
    song_id = "demo_phase4_test_song"

    success = score_manager.save_high_score(
        song_id=song_id,
        score=score_info['final_score'],
        statistics=play_stats
    )

    if success:
        print(f"   [OK] High score saved!")

        # Load and display
        high_score = score_manager.get_high_score(song_id)
        if high_score:
            print(f"      - Saved score: {high_score['score']}")
            print(f"      - Timestamp: {high_score['timestamp']}")

        # Play history
        history = score_manager.get_play_history(song_id, limit=3)
        print(f"      - Play history entries: {len(history)}")

    # 8. Detailed statistics
    print("\n[8] Detailed statistics:")
    print("   " + "-"*66)
    print(f"   {'Metric':<30} | {'Value':>15}")
    print("   " + "-"*66)

    detailed = tracker.get_detailed_stats()
    metrics = [
        ('Total Actions', detailed['total_actions']),
        ('Total Jumps', detailed['total_jumps']),
        ('Total Ducks', detailed['total_ducks']),
        ('Perfect Actions', detailed['total_perfect_actions']),
        ('Perfect Rate', f"{detailed['perfect_rate']:.1f}%"),
        ('Average Combo', f"{detailed['avg_combo']:.1f}"),
        ('Actions per Second', f"{detailed['actions_per_second']:.2f}"),
    ]

    for name, value in metrics:
        print(f"   {name:<30} | {str(value):>15}")

    print("   " + "-"*66)

    # Complete
    print("\n" + "="*70)
    print("  [SUCCESS] Phase 4 Demo Complete!")
    print("  Scoring System:")
    print(f"    - Score Manager: Working")
    print(f"    - Statistics Tracker: Working")
    print(f"    - Difficulty Analyzer: Working")
    print(f"    - High Score Persistence: Working")
    print("  Next: Phase 5 (Polish & MVP)")
    print("="*70 + "\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n[ERROR] Exception occurred: {e}")
        import traceback
        traceback.print_exc()
