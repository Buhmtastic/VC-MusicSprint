# -*- coding: utf-8 -*-
"""
Phase 3 Demo Script
Character & Auto-Play System Test

실행 방법:
python demo_phase3.py
"""

import sys
from pathlib import Path
import numpy as np
import pygame

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from src.audio.audio_analyzer import AudioAnalyzer
from src.course.course_generator import CourseGenerator
from src.game.game import Game, GameState
from src.game.renderer import GameRenderer


def generate_test_audio(duration: float = 10.0, sample_rate: int = 22050):
    """
    테스트용 오디오 생성 (비트감 있는 사인파)

    Args:
        duration: 길이 (초)
        sample_rate: 샘플레이트

    Returns:
        (waveform, sample_rate) 튜플
    """
    t = np.linspace(0, duration, int(sample_rate * duration))

    # 기본 주파수 (440Hz)
    base_freq = 440.0
    waveform = np.sin(2 * np.pi * base_freq * t)

    # 비트 추가 (120 BPM = 2 beats/second)
    beat_freq = 2.0
    beat_envelope = 0.5 + 0.5 * np.sin(2 * np.pi * beat_freq * t)
    waveform = waveform * beat_envelope

    # 진폭 모듈레이션 추가
    amp_mod = 0.7 + 0.3 * np.sin(2 * np.pi * 0.5 * t)
    waveform = waveform * amp_mod

    return waveform, sample_rate


def main():
    """Phase 3 Demo 실행"""
    print("\n" + "="*70)
    print("  Music Sprint - Phase 3 Demo")
    print("  Character & Auto-Play System Test")
    print("="*70 + "\n")

    # 1. Generate test audio
    print("[1] Generating test audio...")
    duration = 10.0
    waveform, sample_rate = generate_test_audio(duration=duration)
    print(f"   [OK] Generated: {duration}s audio")

    # 2. Analyze audio
    print("\n[2] Analyzing audio...")
    analyzer = AudioAnalyzer()
    features = analyzer.analyze(waveform, sample_rate)

    print(f"   [OK] Analysis complete:")
    print(f"      - Duration: {features['duration']:.2f}s")
    print(f"      - Beats: {features['beats']['count']}")
    print(f"      - Tempo: {features['tempo']['bpm']:.1f} BPM")
    print(f"      - Difficulty: {features['difficulty']['level']}")

    # 3. Generate course
    print("\n[3] Generating course...")
    generator = CourseGenerator(seed=42)
    course = generator.generate(features, course_name="Phase 3 Demo Course")

    stats = course.get_statistics()
    print(f"   [OK] Course generated:")
    print(f"      - Total obstacles: {stats['total_obstacles']}")
    print(f"      - Beat obstacles: {stats['by_type']['beat']}")
    print(f"      - Frequency walls: {stats['by_type']['frequency']}")
    print(f"      - Amplitude gaps: {stats['by_type']['amplitude']}")

    # 4. Create game
    print("\n[4] Initializing game...")
    game = Game(course, waveform=waveform, sample_rate=sample_rate)
    renderer = GameRenderer(game)
    print(f"   [OK] Game initialized")

    # 5. Run game loop
    print("\n[5] Starting game loop...")
    print("   Controls:")
    print("      - SPACE: Start game")
    print("      - ESC: Exit")
    print("\n" + "="*70 + "\n")

    # PyGame 이벤트 루프
    running = True
    game_started = False

    while running:
        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    if game.state == GameState.NOT_STARTED:
                        game.start()
                        game_started = True
                        print("[Game Started]")

        # 게임 상태에 따라 렌더링
        if game.state == GameState.NOT_STARTED:
            renderer.render_start_screen()

        elif game.state == GameState.PLAYING:
            delta_time = renderer.get_delta_time()

            # 게임 업데이트
            continues = game.update(delta_time)

            # 렌더링
            renderer.render(delta_time)

            # 게임 종료 체크
            if not continues:
                print("\n[Game Finished]")
                stats = game.get_statistics()
                print(f"   Score: {stats['score']}")
                print(f"   Success Rate: {stats['success_rate']:.1f}%")
                print(f"   Avoided: {stats['obstacles_avoided']}")
                print(f"   Hit: {stats['obstacles_hit']}")

        elif game.state == GameState.FINISHED:
            renderer.render_end_screen()

        else:
            # PAUSED or other states
            renderer.render(0.0)

    # Cleanup
    renderer.cleanup()

    print("\n" + "="*70)
    print("  [SUCCESS] Phase 3 Demo Complete!")
    print("  Next: Phase 4 (Scoring & Results)")
    print("="*70 + "\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n[ERROR] Exception occurred: {e}")
        import traceback
        traceback.print_exc()
