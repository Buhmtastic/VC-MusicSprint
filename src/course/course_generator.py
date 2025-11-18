"""
CourseGenerator 클래스
오디오 분석 데이터로부터 게임 코스를 생성하는 Factory
"""

from typing import Dict, List
import random
from .obstacle import BeatObstacle, FrequencyWall, AmplitudeGap, Obstacle
from .course import Course


class CourseGenerator:
    """
    코스 생성기 (Factory Pattern)

    책임:
    - 오디오 분석 데이터를 입력받아 Course 객체 생성
    - 비트 → 장애물 매핑
    - 주파수 → 장애물 높이 매핑
    - 볼륨 → 장애물 밀도 매핑

    OOP 원칙: Factory Pattern, 단일 책임
    """

    # 생성 설정 상수
    COURSE_WIDTH = 800.0  # 게임 화면 너비 (픽셀)
    BEAT_SPAWN_PROBABILITY = 0.8  # 비트마다 장애물 생성 확률
    FREQUENCY_SAMPLE_RATE = 0.5   # 주파수 장애물 샘플링 간격 (초)
    AMPLITUDE_SAMPLE_RATE = 1.0   # 볼륨 장애물 샘플링 간격 (초)

    def __init__(self, seed: int = None):
        """
        CourseGenerator 초기화

        Args:
            seed: 랜덤 시드 (재현성을 위해)
        """
        self._seed = seed
        if seed is not None:
            random.seed(seed)

    def generate(self, audio_features: Dict, course_name: str = "Generated Course") -> Course:
        """
        오디오 분석 데이터로부터 코스 생성 (Factory 메서드)

        Args:
            audio_features: AudioAnalyzer.analyze() 결과 딕셔너리
            course_name: 생성할 코스 이름

        Returns:
            생성된 Course 객체
        """
        # 코스 생성
        duration = audio_features['duration']
        course = Course(duration=duration, name=course_name)

        # 1. 비트 기반 장애물 생성
        beat_obstacles = self._create_obstacles_from_beats(audio_features['beats'])
        course.add_obstacles(beat_obstacles)

        # 2. 주파수 기반 장애물 생성
        frequency_obstacles = self._create_obstacles_from_frequency(
            audio_features['spectral'],
            duration
        )
        course.add_obstacles(frequency_obstacles)

        # 3. 볼륨 기반 장애물 생성
        amplitude_obstacles = self._create_obstacles_from_amplitude(
            audio_features['amplitude'],
            duration
        )
        course.add_obstacles(amplitude_obstacles)

        # 4. 코스 최종화
        course.finalize()

        return course

    def _create_obstacles_from_beats(self, beat_data: Dict) -> List[BeatObstacle]:
        """
        비트 데이터로부터 BeatObstacle 생성 (private 메서드)

        Args:
            beat_data: AudioAnalyzer의 beats 딕셔너리

        Returns:
            BeatObstacle 리스트
        """
        obstacles = []
        beat_times = beat_data['times']

        for beat_time in beat_times:
            # 확률적으로 장애물 생성 (모든 비트에 장애물을 놓으면 너무 어려움)
            if random.random() < self.BEAT_SPAWN_PROBABILITY:
                # X 위치를 랜덤하게 배치 (화면 중앙 ±30% 범위)
                x_offset = random.uniform(-0.3, 0.3) * self.COURSE_WIDTH
                x_position = (self.COURSE_WIDTH / 2) + x_offset

                # 비트 강도는 랜덤 (실제로는 오디오 RMS 사용 가능)
                beat_strength = random.uniform(0.6, 1.0)

                obstacle = BeatObstacle(
                    time=beat_time,
                    x_position=x_position,
                    beat_strength=beat_strength
                )
                obstacles.append(obstacle)

        return obstacles

    def _create_obstacles_from_frequency(self, spectral_data: Dict, duration: float) -> List[FrequencyWall]:
        """
        주파수 스펙트럼 데이터로부터 FrequencyWall 생성 (private 메서드)

        Args:
            spectral_data: AudioAnalyzer의 spectral 딕셔너리
            duration: 코스 총 길이

        Returns:
            FrequencyWall 리스트
        """
        obstacles = []
        centroid_values = spectral_data['centroid']['values']

        # 주파수 장애물은 일정 간격으로 샘플링
        num_samples = int(duration / self.FREQUENCY_SAMPLE_RATE)

        for i in range(num_samples):
            time = i * self.FREQUENCY_SAMPLE_RATE

            # 해당 시간의 spectral centroid 값 가져오기
            # (centroid_values는 프레임 단위이므로 보간 필요)
            frame_index = int((time / duration) * len(centroid_values))
            frame_index = min(frame_index, len(centroid_values) - 1)

            frequency = centroid_values[frame_index]

            # X 위치 배치 (화면 양쪽에 번갈아 배치)
            if i % 2 == 0:
                x_position = self.COURSE_WIDTH * 0.25  # 왼쪽
            else:
                x_position = self.COURSE_WIDTH * 0.75  # 오른쪽

            obstacle = FrequencyWall(
                time=time,
                x_position=x_position,
                frequency=frequency,
                max_frequency=spectral_data['centroid']['mean'] * 2  # 평균의 2배를 최대값으로
            )
            obstacles.append(obstacle)

        return obstacles

    def _create_obstacles_from_amplitude(self, amplitude_data: Dict, duration: float) -> List[AmplitudeGap]:
        """
        볼륨 데이터로부터 AmplitudeGap 생성 (private 메서드)

        Args:
            amplitude_data: AudioAnalyzer의 amplitude 딕셔너리
            duration: 코스 총 길이

        Returns:
            AmplitudeGap 리스트
        """
        obstacles = []
        rms_values = amplitude_data['rms']
        rms_mean = amplitude_data['mean']
        rms_max = amplitude_data['max']

        # 볼륨 장애물은 더 긴 간격으로 샘플링
        num_samples = int(duration / self.AMPLITUDE_SAMPLE_RATE)

        for i in range(num_samples):
            time = i * self.AMPLITUDE_SAMPLE_RATE

            # 해당 시간의 RMS 값 가져오기
            frame_index = int((time / duration) * len(rms_values))
            frame_index = min(frame_index, len(rms_values) - 1)

            rms = rms_values[frame_index]

            # RMS를 0~1로 정규화
            normalized_amplitude = min(rms / rms_max, 1.0) if rms_max > 0 else 0.5

            # X 위치 (화면 중앙)
            x_position = self.COURSE_WIDTH / 2

            # 볼륨이 평균보다 큰 경우에만 생성 (선택적)
            if rms > rms_mean * 0.8:  # 평균의 80% 이상일 때만
                obstacle = AmplitudeGap(
                    time=time,
                    x_position=x_position,
                    amplitude=normalized_amplitude
                )
                obstacles.append(obstacle)

        return obstacles

    def _create_background_from_spectral(self, spectral_data: Dict) -> Dict:
        """
        주파수 스펙트럼으로부터 배경 색상 데이터 생성 (private 메서드)
        Phase 2에서는 미구현, Phase 3에서 활용 예정

        Args:
            spectral_data: 스펙트럼 데이터

        Returns:
            배경 정보 딕셔너리
        """
        # TODO: Phase 3에서 구현
        return {
            'base_color': (20, 20, 40),  # 어두운 파란색 배경
            'dynamic': False
        }

    def get_generation_stats(self, course: Course) -> Dict:
        """
        생성된 코스의 통계 정보

        Args:
            course: 생성된 코스

        Returns:
            생성 통계 딕셔너리
        """
        stats = course.get_statistics()

        # 추가 메타데이터
        stats['generator'] = 'CourseGenerator'
        stats['seed'] = self._seed

        return stats

    @staticmethod
    def create_empty_course(duration: float, name: str = "Empty Course") -> Course:
        """
        빈 코스 생성 (정적 팩토리 메서드)

        Args:
            duration: 코스 길이
            name: 코스 이름

        Returns:
            빈 Course 객체
        """
        course = Course(duration=duration, name=name)
        course.finalize()
        return course
