#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Music Sprint - Phase 5 Demo
통합 데모: 전체 파이프라인 (Audio → Course → Game → Results)

Phase 5 핵심 기능:
- 전체 파이프라인 통합
- 향상된 결과 화면 (matplotlib 그래프)
- 하이스코어 저장 및 비교
- MVP 기능 완성
"""

import sys
import os
import time
import pygame
import numpy as np

# 프로젝트 루트 경로 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.audio.audio_analyzer import AudioAnalyzer
from src.course.course_generator import CourseGenerator
from src.game.game import Game, GameState
from src.game.renderer import GameRenderer
from src.score.score_manager import ScoreManager
from src.ui.result_screen import ResultScreen


def generate_test_audio(duration: float = 15.0, sample_rate: int = 22050):
    """
    테스트용 오디오 생성 (비트 패턴 포함)

    Args:
        duration: 오디오 길이 (초)
        sample_rate: 샘플레이트

    Returns:
        (waveform, sample_rate)
    """
    print("\n[1] Generating test audio...")
    t = np.linspace(0, duration, int(duration * sample_rate))

    # 베이스 주파수
    base_freq = 220  # A3

    # 멜로디 생성 (비트 패턴)
    waveform = np.zeros_like(t)

    # 비트 간격 (0.5초마다)
    beat_interval = 0.5
    num_beats = int(duration / beat_interval)

    for i in range(num_beats):
        beat_time = i * beat_interval
        beat_start = int(beat_time * sample_rate)
        beat_end = int((beat_time + 0.1) * sample_rate)

        # 비트 사운드 (짧은 톤)
        beat_samples = t[beat_start:beat_end] - beat_time
        frequency = base_freq * (1 + (i % 4) * 0.25)  # 음높이 변화
        waveform[beat_start:beat_end] = np.sin(2 * np.pi * frequency * beat_samples)

    # 볼륨 정규화
    waveform = waveform * 0.5

    print(f"   ✓ Audio generated: {duration}s, {sample_rate}Hz")
    return waveform, sample_rate


def run_full_pipeline_demo():
    """전체 파이프라인 데모 실행"""
    print("="*60)
    print("Music Sprint - Phase 5: Full Pipeline Demo")
    print("="*60)

    # ============================================================
    # Step 1: Audio Generation
    # ============================================================
    waveform, sample_rate = generate_test_audio(duration=15.0)

    # ============================================================
    # Step 2: Audio Analysis
    # ============================================================
    print("\n[2] Analyzing audio...")
    analyzer = AudioAnalyzer()
    features = analyzer.analyze(waveform, sample_rate)

    print(f"   ✓ BPM: {features['tempo']['bpm']:.1f}")
    print(f"   ✓ Beats detected: {features['beats']['count']}")
    print(f"   ✓ Duration: {features['duration']:.1f}s")

    # ============================================================
    # Step 3: Course Generation
    # ============================================================
    print("\n[3] Generating course...")
    generator = CourseGenerator()
    course = generator.generate(features)

    print(f"   ✓ Total obstacles: {course.obstacle_count}")
    print(f"   ✓ Course density: {course.obstacle_count / course.duration:.1f} obs/s")

    # ============================================================
    # Step 4: Game Initialization
    # ============================================================
    print("\n[4] Initializing game...")
    game = Game(course, waveform, sample_rate)
    renderer = GameRenderer(game)

    print(f"   ✓ Difficulty: {game.difficulty_level.upper()}")
    print(f"   ✓ Game ready!")

    # ============================================================
    # Step 5: Game Loop (PyGame)
    # ============================================================
    print("\n[5] Starting game loop...")
    print("   Controls: SPACE = Start, ESC = Exit")

    # 시작 화면
    waiting_for_start = True
    while waiting_for_start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                renderer.cleanup()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    renderer.cleanup()
                    return
                elif event.key == pygame.K_SPACE:
                    waiting_for_start = False

        renderer.render_start_screen()

    # 게임 시작
    game.start()
    running = True
    clock = pygame.time.Clock()

    while running:
        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # 게임 업데이트
        delta_time = renderer.get_delta_time()
        continue_playing = game.update(delta_time)

        # 렌더링
        renderer.render(delta_time)

        # 게임 종료 체크
        if not continue_playing:
            print("\n   ✓ Game finished!")
            break

        clock.tick(60)

    # ============================================================
    # Step 6: Result Screen with Graphs
    # ============================================================
    print("\n[6] Displaying results...")

    # 게임 통계 수집
    game_stats = game.get_statistics()
    stats_summary = game.statistics_tracker.get_summary()

    # 최종 점수 계산
    score_manager = game.score_manager
    song_id = "demo_phase5_test_song"

    score_info = score_manager.calculate_final_score(
        obstacles_avoided=stats_summary['obstacles_avoided'],
        perfect_dodges=game_stats['perfect_dodges'],
        max_combo=stats_summary['max_combo'],
        accuracy=stats_summary['timing_accuracy'],
        difficulty_level=game.difficulty_level
    )

    # 하이스코어 로드
    high_score_data = score_manager.get_high_score(song_id)

    # 하이스코어 저장
    score_manager.save_high_score(
        song_id=song_id,
        score=score_info['final_score'],
        difficulty_level=game.difficulty_level,
        stats=stats_summary
    )

    # 결과 화면 생성
    result_screen = ResultScreen()
    result_path = result_screen.display_and_save(
        game_stats=game_stats,
        score_info=score_info,
        high_score_data=high_score_data,
        filename='phase5_demo_result.png'
    )

    print(f"   ✓ Result screen saved: {result_path}")

    # ============================================================
    # Step 7: Summary
    # ============================================================
    print("\n" + "="*60)
    print("DEMO COMPLETE - Summary")
    print("="*60)
    print(f"Final Score:        {score_info['final_score']:,}")
    print(f"Difficulty:         {game.difficulty_level.upper()}")
    print(f"Success Rate:       {game_stats['success_rate']:.1f}%")
    print(f"Max Combo:          {stats_summary['max_combo']}")
    print(f"Timing Accuracy:    {stats_summary['timing_accuracy']*100:.1f}%")
    print(f"Obstacles Avoided:  {stats_summary['obstacles_avoided']}")
    print(f"Obstacles Hit:      {stats_summary['obstacles_hit']}")
    print("="*60)

    # 결과 화면 대기
    print("\nClose the matplotlib window to exit...")
    input("Press ENTER to close...")

    # 정리
    result_screen.close()
    renderer.cleanup()
    pygame.quit()

    print("\n✅ Phase 5 Demo Completed Successfully!")


if __name__ == '__main__':
    try:
        run_full_pipeline_demo()
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
        pygame.quit()
    except Exception as e:
        print(f"\n\n❌ Error occurred: {e}")
        import traceback
        traceback.print_exc()
        pygame.quit()
