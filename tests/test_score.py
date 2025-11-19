# -*- coding: utf-8 -*-
"""
Phase 4 Tests: 점수 및 통계 시스템

테스트 범위:
- ScoreManager (점수 계산, 하이스코어)
- StatisticsTracker (통계 수집)
- DifficultyAnalyzer (난이도 분석)
"""

import pytest
import sys
from pathlib import Path
import json
import tempfile
import shutil

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.score.score_manager import ScoreManager
from src.score.statistics_tracker import StatisticsTracker
from src.score.difficulty_analyzer import DifficultyAnalyzer
from src.course.course import Course
from src.course.obstacle import BeatObstacle


# ============================================================================
# ScoreManager Tests
# ============================================================================

class TestScoreManager:
    """ScoreManager 클래스 테스트"""

    def test_initialization(self):
        """초기화 테스트"""
        manager = ScoreManager()
        assert manager.current_score == 0
        assert manager.current_difficulty_multiplier == 1.0

    def test_calculate_score_basic(self):
        """기본 점수 계산 테스트"""
        manager = ScoreManager()
        score = manager.calculate_score(
            obstacles_avoided=10,
            perfect_dodges=0,
            current_combo=0,
            accuracy=1.0
        )

        expected = 10 * manager.BASE_SCORE_PER_OBSTACLE
        assert score == expected

    def test_calculate_score_with_perfect_dodges(self):
        """완벽한 회피 보너스 테스트"""
        manager = ScoreManager()
        score = manager.calculate_score(
            obstacles_avoided=10,
            perfect_dodges=5,
            current_combo=0,
            accuracy=1.0
        )

        expected_base = 10 * manager.BASE_SCORE_PER_OBSTACLE
        expected_bonus = 5 * manager.PERFECT_DODGE_BONUS
        assert score >= expected_base + expected_bonus

    def test_calculate_score_with_combo(self):
        """콤보 배율 테스트"""
        manager = ScoreManager()

        # 콤보 없음
        score_no_combo = manager.calculate_score(
            obstacles_avoided=10,
            perfect_dodges=0,
            current_combo=0,
            accuracy=1.0
        )

        # 콤보 10
        score_with_combo = manager.calculate_score(
            obstacles_avoided=10,
            perfect_dodges=0,
            current_combo=10,
            accuracy=1.0
        )

        # 콤보 있을 때 점수가 더 높아야 함
        assert score_with_combo > score_no_combo

    def test_apply_difficulty_multiplier(self):
        """난이도 배율 적용 테스트"""
        manager = ScoreManager()
        base_score = 100

        easy_score = manager.apply_difficulty_multiplier(base_score, 'easy')
        hard_score = manager.apply_difficulty_multiplier(base_score, 'hard')

        assert easy_score == 100  # 1.0x
        assert hard_score == 200  # 2.0x

    def test_calculate_final_score(self):
        """최종 점수 계산 테스트"""
        manager = ScoreManager()

        result = manager.calculate_final_score(
            obstacles_avoided=20,
            perfect_dodges=5,
            max_combo=10,
            accuracy=0.9,
            difficulty_level='normal'
        )

        assert 'base_score' in result
        assert 'final_score' in result
        assert 'difficulty_multiplier' in result
        assert result['final_score'] >= result['base_score']

    def test_save_and_load_high_score(self, tmp_path):
        """하이스코어 저장/로드 테스트"""
        # 임시 디렉토리 사용
        original_dir = ScoreManager.SCORES_DIR
        ScoreManager.SCORES_DIR = tmp_path

        try:
            manager = ScoreManager()
            song_id = "test_song_123"
            score = 1000

            # 저장
            success = manager.save_high_score(song_id, score)
            assert success is True

            # 로드
            high_score = manager.get_high_score(song_id)
            assert high_score is not None
            assert high_score['score'] == score

        finally:
            ScoreManager.SCORES_DIR = original_dir

    def test_play_history(self, tmp_path):
        """플레이 기록 테스트"""
        original_dir = ScoreManager.SCORES_DIR
        ScoreManager.SCORES_DIR = tmp_path

        try:
            manager = ScoreManager()
            song_id = "test_song_456"

            # 여러 번 플레이 기록
            for score in [100, 200, 300]:
                manager.save_high_score(song_id, score)

            # 기록 조회
            history = manager.get_play_history(song_id, limit=5)
            assert len(history) == 3
            assert history[0]['score'] == 300  # 최신순

        finally:
            ScoreManager.SCORES_DIR = original_dir


# ============================================================================
# StatisticsTracker Tests
# ============================================================================

class TestStatisticsTracker:
    """StatisticsTracker 클래스 테스트"""

    def test_initialization(self):
        """초기화 테스트"""
        tracker = StatisticsTracker()
        assert tracker.current_combo == 0
        assert tracker.max_combo == 0
        assert tracker.obstacles_avoided == 0

    def test_track_jump(self):
        """점프 추적 테스트"""
        tracker = StatisticsTracker()

        tracker.track_jump(is_perfect=False)
        tracker.track_jump(is_perfect=True)

        summary = tracker.get_summary()
        assert summary['total_jumps'] == 2
        assert summary['perfect_jumps'] == 1

    def test_track_duck(self):
        """숙이기 추적 테스트"""
        tracker = StatisticsTracker()

        tracker.track_duck(is_perfect=True)
        tracker.track_duck(is_perfect=False)

        summary = tracker.get_summary()
        assert summary['total_ducks'] == 2
        assert summary['perfect_ducks'] == 1

    def test_track_obstacle_avoided(self):
        """장애물 회피 추적 테스트"""
        tracker = StatisticsTracker()

        tracker.track_obstacle_avoided()
        tracker.track_obstacle_avoided()

        assert tracker.obstacles_avoided == 2
        assert tracker.current_combo == 2

    def test_track_obstacle_hit_resets_combo(self):
        """장애물 충돌 시 콤보 리셋 테스트"""
        tracker = StatisticsTracker()

        # 콤보 쌓기
        tracker.track_obstacle_avoided()
        tracker.track_obstacle_avoided()
        tracker.track_obstacle_avoided()
        assert tracker.current_combo == 3

        # 충돌
        tracker.track_obstacle_hit()
        assert tracker.current_combo == 0
        assert tracker.obstacles_hit == 1

    def test_max_combo_tracking(self):
        """최대 콤보 추적 테스트"""
        tracker = StatisticsTracker()

        # 첫 번째 콤보
        for _ in range(5):
            tracker.track_obstacle_avoided()
        assert tracker.max_combo == 5

        # 리셋
        tracker.track_obstacle_hit()

        # 더 큰 콤보
        for _ in range(10):
            tracker.track_obstacle_avoided()
        assert tracker.max_combo == 10

    def test_success_rate_calculation(self):
        """성공률 계산 테스트"""
        tracker = StatisticsTracker()

        # 10번 회피, 2번 충돌
        for _ in range(10):
            tracker.track_obstacle_avoided()
        for _ in range(2):
            tracker.track_obstacle_hit()

        summary = tracker.get_summary()
        expected_rate = (10 / 12) * 100.0
        assert abs(summary['success_rate'] - expected_rate) < 0.01

    def test_timing_accuracy_tracking(self):
        """타이밍 정확도 추적 테스트"""
        tracker = StatisticsTracker()

        tracker.track_jump(timing_accuracy=1.0)
        tracker.track_jump(timing_accuracy=0.8)
        tracker.track_jump(timing_accuracy=0.9)

        summary = tracker.get_summary()
        expected_avg = (1.0 + 0.8 + 0.9) / 3
        assert abs(summary['timing_accuracy'] - expected_avg) < 0.01

    def test_get_detailed_stats(self):
        """상세 통계 반환 테스트"""
        tracker = StatisticsTracker()

        tracker.track_jump()
        tracker.track_duck()
        tracker.track_obstacle_avoided()

        detailed = tracker.get_detailed_stats()
        assert 'combo_history' in detailed
        assert 'timing_accuracy_history' in detailed
        assert isinstance(detailed['combo_history'], list)

    def test_reset(self):
        """통계 초기화 테스트"""
        tracker = StatisticsTracker()

        tracker.track_jump()
        tracker.track_obstacle_avoided()

        tracker.reset()

        assert tracker.current_combo == 0
        assert tracker.obstacles_avoided == 0


# ============================================================================
# DifficultyAnalyzer Tests
# ============================================================================

class TestDifficultyAnalyzer:
    """DifficultyAnalyzer 클래스 테스트"""

    def test_initialization(self):
        """초기화 테스트"""
        analyzer = DifficultyAnalyzer()
        assert analyzer.last_analysis == {}

    def test_analyze_difficulty_from_features(self):
        """오디오 features로부터 난이도 분석 테스트"""
        analyzer = DifficultyAnalyzer()

        # 샘플 features
        features = {
            'tempo': {'bpm': 120.0},
            'beats': {'count': 100},
            'duration': 60.0,
            'spectral': {
                'centroid': 1000.0,
                'rolloff': 2000.0
            }
        }

        result = analyzer.analyze_difficulty(features)

        assert 'difficulty_score' in result
        assert 'difficulty_level' in result
        assert result['difficulty_level'] in ['easy', 'normal', 'hard', 'expert']

    def test_analyze_difficulty_from_course(self):
        """Course로부터 난이도 분석 테스트"""
        analyzer = DifficultyAnalyzer()

        # 간단한 코스 생성
        course = Course(duration=10.0, name="Test Course")
        course.add_obstacle(BeatObstacle(time=1.0, x_position=100.0, beat_strength=0.8))
        course.add_obstacle(BeatObstacle(time=2.0, x_position=100.0, beat_strength=0.9))
        course.finalize()

        result = analyzer.analyze_difficulty_from_course(course)

        assert 'difficulty_score' in result
        assert 'difficulty_level' in result
        assert 'components' in result

    def test_difficulty_levels(self):
        """난이도 레벨 판정 테스트"""
        analyzer = DifficultyAnalyzer()

        # Easy features
        easy_features = {
            'tempo': {'bpm': 80.0},
            'beats': {'count': 30},
            'duration': 60.0,
            'spectral': {'centroid': 500.0, 'rolloff': 600.0}
        }

        result_easy = analyzer.analyze_difficulty(easy_features)
        assert result_easy['difficulty_level'] in ['easy', 'normal']

        # Hard features
        hard_features = {
            'tempo': {'bpm': 180.0},
            'beats': {'count': 200},
            'duration': 60.0,
            'spectral': {'centroid': 2000.0, 'rolloff': 4000.0}
        }

        result_hard = analyzer.analyze_difficulty(hard_features)
        # Hard features should result in higher difficulty
        assert result_hard['difficulty_score'] > result_easy['difficulty_score']

    def test_get_difficulty_description(self):
        """난이도 설명 반환 테스트"""
        analyzer = DifficultyAnalyzer()

        desc_easy = analyzer.get_difficulty_description('easy')
        desc_hard = analyzer.get_difficulty_description('hard')

        assert isinstance(desc_easy, str)
        assert len(desc_easy) > 0
        assert isinstance(desc_hard, str)


# ============================================================================
# Integration Tests
# ============================================================================

class TestIntegration:
    """통합 테스트"""

    def test_score_and_statistics_integration(self):
        """ScoreManager와 StatisticsTracker 통합 테스트"""
        manager = ScoreManager()
        tracker = StatisticsTracker()

        # 게임 시뮬레이션
        for _ in range(20):
            tracker.track_obstacle_avoided()

        for _ in range(3):
            tracker.track_obstacle_hit()

        # 통계 요약
        stats = tracker.get_summary()

        # 최종 점수 계산
        final = manager.calculate_final_score(
            obstacles_avoided=stats['obstacles_avoided'],
            perfect_dodges=0,
            max_combo=stats['max_combo'],
            accuracy=stats['timing_accuracy'],
            difficulty_level='normal'
        )

        assert final['final_score'] > 0
        assert final['obstacles_avoided'] == 20


# ============================================================================
# Run Tests
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
