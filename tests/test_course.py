"""
Course 모듈 테스트
Phase 2: 코스 생성 시스템
"""

import pytest
import numpy as np
from pathlib import Path
import sys

# 프로젝트 루트를 경로에 추가
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.course.obstacle import (
    Obstacle, BeatObstacle, FrequencyWall, AmplitudeGap, ObstacleType
)
from src.course.course import Course
from src.course.course_generator import CourseGenerator
from src.audio.audio_analyzer import AudioAnalyzer


class TestObstacle:
    """Obstacle 클래스 계층 테스트"""

    def test_beat_obstacle(self):
        """BeatObstacle 생성 및 속성 테스트"""
        obstacle = BeatObstacle(time=1.0, x_position=400.0, beat_strength=0.8)

        assert obstacle.time == 1.0
        assert obstacle.x_position == 400.0
        assert obstacle.beat_strength == 0.8
        assert obstacle.get_type() == ObstacleType.BEAT
        assert obstacle.get_height() > 0
        assert obstacle.get_width() > 0
        assert len(obstacle.get_color()) == 3  # RGB 튜플

    def test_frequency_wall(self):
        """FrequencyWall 생성 및 높이 매핑 테스트"""
        # 저음
        low_freq = FrequencyWall(time=1.0, x_position=200.0, frequency=500.0, max_frequency=5000.0)
        # 고음
        high_freq = FrequencyWall(time=2.0, x_position=200.0, frequency=4000.0, max_frequency=5000.0)

        # 고음이 더 높아야 함
        assert high_freq.get_height() > low_freq.get_height()
        assert high_freq.get_type() == ObstacleType.FREQUENCY

    def test_amplitude_gap(self):
        """AmplitudeGap 생성 및 볼륨 매핑 테스트"""
        # 작은 볼륨
        quiet = AmplitudeGap(time=1.0, x_position=400.0, amplitude=0.3)
        # 큰 볼륨
        loud = AmplitudeGap(time=2.0, x_position=400.0, amplitude=0.9)

        # 볼륨이 클수록 간격이 넓어야 함
        assert loud.get_height() > quiet.get_height()
        assert loud.get_type() == ObstacleType.AMPLITUDE

    def test_polymorphism(self):
        """다형성 테스트: 모든 Obstacle을 동일하게 처리"""
        obstacles = [
            BeatObstacle(1.0, 400.0, 0.8),
            FrequencyWall(2.0, 200.0, 2000.0),
            AmplitudeGap(3.0, 400.0, 0.7)
        ]

        for obs in obstacles:
            # 모든 Obstacle이 공통 인터페이스 구현
            assert isinstance(obs, Obstacle)
            assert obs.get_height() > 0
            assert obs.get_width() > 0
            assert isinstance(obs.get_type(), ObstacleType)
            assert len(obs.get_color()) == 3

            info = obs.get_info()
            assert 'type' in info
            assert 'time' in info


class TestCourse:
    """Course 클래스 테스트"""

    def test_course_creation(self):
        """코스 생성 테스트"""
        course = Course(duration=10.0, name="Test Course")

        assert course.duration == 10.0
        assert course.name == "Test Course"
        assert course.obstacle_count == 0
        assert not course.is_finalized

    def test_add_obstacles(self):
        """장애물 추가 테스트"""
        course = Course(duration=10.0)

        obstacle1 = BeatObstacle(1.0, 400.0, 0.8)
        obstacle2 = FrequencyWall(2.0, 200.0, 2000.0)

        course.add_obstacle(obstacle1)
        course.add_obstacle(obstacle2)

        assert course.obstacle_count == 2

    def test_finalize(self):
        """코스 최종화 테스트"""
        course = Course(duration=10.0)

        # 무작위 순서로 장애물 추가
        course.add_obstacle(BeatObstacle(5.0, 400.0, 0.8))
        course.add_obstacle(BeatObstacle(2.0, 400.0, 0.7))
        course.add_obstacle(BeatObstacle(8.0, 400.0, 0.9))

        course.finalize()

        assert course.is_finalized
        # 시간 순으로 정렬되었는지 확인
        assert course.obstacles[0].time == 2.0
        assert course.obstacles[1].time == 5.0
        assert course.obstacles[2].time == 8.0

    def test_get_obstacles_at_time(self):
        """특정 시간의 장애물 조회 테스트"""
        course = Course(duration=10.0)

        course.add_obstacle(BeatObstacle(2.0, 400.0, 0.8))
        course.add_obstacle(BeatObstacle(2.1, 400.0, 0.7))
        course.add_obstacle(BeatObstacle(5.0, 400.0, 0.9))

        course.finalize()

        # 2초 근처 장애물 조회
        obstacles_at_2s = course.get_obstacles_at_time(2.0, tolerance=0.2)
        assert len(obstacles_at_2s) == 2  # 2.0, 2.1 모두 포함

    def test_statistics(self):
        """통계 정보 테스트"""
        course = Course(duration=10.0, name="Stats Test")

        course.add_obstacle(BeatObstacle(1.0, 400.0, 0.8))
        course.add_obstacle(FrequencyWall(2.0, 200.0, 2000.0))
        course.add_obstacle(AmplitudeGap(3.0, 400.0, 0.7))

        course.finalize()

        stats = course.get_statistics()

        assert stats['name'] == "Stats Test"
        assert stats['duration'] == 10.0
        assert stats['total_obstacles'] == 3
        assert stats['by_type']['beat'] == 1
        assert stats['by_type']['frequency'] == 1
        assert stats['by_type']['amplitude'] == 1
        assert stats['density'] == 0.3  # 3 obstacles / 10 seconds


class TestCourseGenerator:
    """CourseGenerator 클래스 테스트"""

    def test_generator_creation(self):
        """생성기 초기화 테스트"""
        generator = CourseGenerator(seed=42)
        assert generator._seed == 42

    def test_generate_from_audio_features(self):
        """오디오 분석 데이터로부터 코스 생성 테스트"""
        # 더미 오디오 데이터 생성 (1초짜리 440Hz 사인파)
        sample_rate = 22050
        duration = 2.0
        t = np.linspace(0, duration, int(sample_rate * duration))
        waveform = np.sin(2 * np.pi * 440 * t)

        # 분석
        analyzer = AudioAnalyzer()
        features = analyzer.analyze(waveform, sample_rate)

        # 코스 생성
        generator = CourseGenerator(seed=42)
        course = generator.generate(features, course_name="Test Generated Course")

        # 검증
        assert course.is_finalized
        assert course.name == "Test Generated Course"
        assert course.duration == pytest.approx(duration, rel=0.1)
        assert course.obstacle_count > 0  # 장애물이 생성되었는지 확인

        # 타입별 장애물 확인
        stats = course.get_statistics()
        print(f"\n생성된 코스 통계: {stats}")

        assert stats['total_obstacles'] > 0

    def test_empty_course_creation(self):
        """빈 코스 생성 테스트 (정적 팩토리 메서드)"""
        empty_course = CourseGenerator.create_empty_course(duration=5.0, name="Empty")

        assert empty_course.is_finalized
        assert empty_course.obstacle_count == 0
        assert empty_course.duration == 5.0


def test_phase2_integration():
    """Phase 2 전체 파이프라인 통합 테스트"""
    print("\n" + "="*60)
    print("  Phase 2 통합 테스트: 오디오 → 코스 생성")
    print("="*60)

    # 1. 더미 오디오 생성
    sample_rate = 22050
    duration = 3.0
    frequency = 440.0

    t = np.linspace(0, duration, int(sample_rate * duration))
    # 비트를 만들기 위해 엔벨로프 추가
    envelope = 0.5 + 0.5 * np.sin(2 * np.pi * 2 * t)  # 2Hz 모듈레이션
    waveform = envelope * np.sin(2 * np.pi * frequency * t)

    print(f"\n1️⃣  더미 오디오 생성: {duration}초, {frequency}Hz")

    # 2. 오디오 분석
    analyzer = AudioAnalyzer()
    features = analyzer.analyze(waveform, sample_rate)

    print(f"2️⃣  오디오 분석 완료:")
    print(f"   - 비트 개수: {features['beats']['count']}")
    print(f"   - 템포: {features['tempo']['bpm']:.1f} BPM")
    print(f"   - 난이도: {features['difficulty']['level']}")

    # 3. 코스 생성
    generator = CourseGenerator(seed=42)
    course = generator.generate(features, course_name="Integration Test Course")

    print(f"3️⃣  코스 생성 완료:")
    stats = course.get_statistics()
    print(f"   - 총 장애물: {stats['total_obstacles']}개")
    print(f"   - Beat 장애물: {stats['by_type']['beat']}개")
    print(f"   - Frequency 장애물: {stats['by_type']['frequency']}개")
    print(f"   - Amplitude 장애물: {stats['by_type']['amplitude']}개")
    print(f"   - 밀도: {stats['density']:.2f} obs/sec")

    # 4. 시각화 테스트 (파일 저장만, 표시 안 함)
    try:
        from src.course.visualizer import CourseVisualizer

        visualizer = CourseVisualizer()
        output_path = "assets/test_course_visualization.png"

        visualizer.visualize(course, output_path=output_path, show=False)
        print(f"4️⃣  시각화 완료: {output_path}")

    except ImportError:
        print("4️⃣  시각화 스킵 (matplotlib 미설치)")

    # 검증
    assert course.obstacle_count > 0
    assert course.is_finalized
    assert stats['total_obstacles'] > 0

    print("\n✅ Phase 2 통합 테스트 성공!")
    print("="*60)


if __name__ == "__main__":
    # pytest 없이 직접 실행 시
    print("🧪 Phase 2 통합 테스트 실행...\n")
    test_phase2_integration()
