# -*- coding: utf-8 -*-
"""
Phase 2 Demo Script
Course Generation System Test
"""

import sys
from pathlib import Path
import numpy as np

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from src.audio.audio_analyzer import AudioAnalyzer
from src.course.course_generator import CourseGenerator
from src.course.visualizer import CourseVisualizer


def main():
    """Phase 2 Demo Execution"""
    print("\n" + "="*70)
    print("  Music Sprint - Phase 2 Demo")
    print("  Course Generation System Test")
    print("="*70 + "\n")

    # 1. Generate dummy audio
    print("[1] Generating dummy audio data...")
    sample_rate = 22050
    duration = 5.0
    frequency = 440.0

    t = np.linspace(0, duration, int(sample_rate * duration))

    # 비트감 있는 사인파 (엔벨로프 추가)
    envelope = 0.5 + 0.5 * np.sin(2 * np.pi * 3 * t)  # 3Hz 모듈레이션
    waveform = envelope * np.sin(2 * np.pi * frequency * t)

    print(f"   [OK] Generated: {duration}s, {frequency}Hz")

    # 2. Audio analysis
    print("\n[2] Analyzing audio...")
    analyzer = AudioAnalyzer()
    features = analyzer.analyze(waveform, sample_rate)

    print(f"   [OK] Analysis complete:")
    print(f"      - Duration: {features['duration']:.2f}s")
    print(f"      - Beats: {features['beats']['count']}")
    print(f"      - Tempo: {features['tempo']['bpm']:.1f} BPM")
    print(f"      - Difficulty: {features['difficulty']['level']} ({features['difficulty']['score']:.1f}/100)")

    # 3. Course generation
    print("\n[3] Generating course...")
    generator = CourseGenerator(seed=42)
    course = generator.generate(features, course_name="Demo Course - 440Hz")

    stats = course.get_statistics()
    print(f"   [OK] Course generation complete:")
    print(f"      - Total obstacles: {stats['total_obstacles']}")
    print(f"      - Beat obstacles: {stats['by_type']['beat']}")
    print(f"      - Frequency obstacles: {stats['by_type']['frequency']}")
    print(f"      - Amplitude obstacles: {stats['by_type']['amplitude']}")
    print(f"      - Density: {stats['density']:.2f} obstacles/sec")

    # 4. Course visualization
    print("\n[4] Visualizing course...")
    visualizer = CourseVisualizer()

    output_path = "assets/phase2_demo_course.png"
    visualizer.visualize(course, output_path=output_path, show=False)

    print(f"   [OK] Visualization saved: {output_path}")

    # 5. Obstacle samples
    print("\n[5] Obstacle Samples (first 10):")
    print("   " + "-"*66)
    print(f"   {'Time':>8} | {'Type':^12} | {'Height':>8} | {'Color':^15}")
    print("   " + "-"*66)

    for i, obstacle in enumerate(course.obstacles[:10]):
        info = obstacle.get_info()
        print(f"   {info['time']:>8.2f}s | {info['type']:^12} | "
              f"{info['height']:>8.1f} | {str(info['color']):^15}")

    if course.obstacle_count > 10:
        print(f"   ... (total {course.obstacle_count} obstacles)")
    print("   " + "-"*66)

    # 6. Polymorphism demo
    print("\n[6] Polymorphism Test:")
    print("   All Obstacle types can be handled uniformly")

    sample_obstacles = course.obstacles[:5]
    for obs in sample_obstacles:
        # All Obstacles provide the same interface
        print(f"   - {obs.get_type().value:12} @ {obs.time:.2f}s: "
              f"height={obs.get_height():.1f}, color={obs.get_color()}")

    # Complete
    print("\n" + "="*70)
    print("  [SUCCESS] Phase 2 Demo Complete!")
    print("  Next: Phase 3 (Character & Auto-Play)")
    print("="*70 + "\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n[ERROR] Exception occurred: {e}")
        import traceback
        traceback.print_exc()
