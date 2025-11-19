# -*- coding: utf-8 -*-
"""
DifficultyAnalyzer Class
곡 난이도 분석 및 판정

책임:
- BPM, 주파수 분산, 비트 밀도 기반 난이도 계산
- 난이도 레벨 판정 (easy/normal/hard/expert)
- 난이도 점수 계산
"""

from typing import Dict
import numpy as np


class DifficultyAnalyzer:
    """
    난이도 분석 클래스

    OOP 원칙:
    - 단일 책임: 난이도 분석만 담당
    - 캡슐화: 분석 알고리즘 내부 은닉
    """

    # 난이도 판정 임계값
    DIFFICULTY_THRESHOLDS = {
        'easy': 30.0,
        'normal': 50.0,
        'hard': 70.0,
        'expert': 85.0
    }

    # 가중치 (BPM, 주파수 분산, 비트 밀도)
    WEIGHT_BPM = 0.4
    WEIGHT_FREQUENCY_VARIANCE = 0.3
    WEIGHT_BEAT_DENSITY = 0.3

    # BPM 범위 (정규화용)
    BPM_MIN = 60.0
    BPM_MAX = 200.0

    # 비트 밀도 범위 (beats/second)
    BEAT_DENSITY_MIN = 0.5
    BEAT_DENSITY_MAX = 4.0

    def __init__(self):
        """DifficultyAnalyzer 초기화"""
        self._last_analysis: Dict = {}

    # ============================================================
    # Public Methods - 난이도 분석
    # ============================================================

    def analyze_difficulty(self, audio_features: Dict) -> Dict:
        """
        오디오 features로부터 난이도 분석

        Args:
            audio_features: AudioAnalyzer의 분석 결과

        Returns:
            난이도 분석 결과 딕셔너리
        """
        # BPM 점수 계산
        bpm_score = self._calculate_bpm_score(audio_features)

        # 주파수 분산 점수 계산
        freq_variance_score = self._calculate_frequency_variance_score(audio_features)

        # 비트 밀도 점수 계산
        beat_density_score = self._calculate_beat_density_score(audio_features)

        # 가중 평균으로 최종 난이도 점수 계산
        final_score = (
            bpm_score * self.WEIGHT_BPM +
            freq_variance_score * self.WEIGHT_FREQUENCY_VARIANCE +
            beat_density_score * self.WEIGHT_BEAT_DENSITY
        )

        # 난이도 레벨 판정
        difficulty_level = self._determine_difficulty_level(final_score)

        # 결과 저장
        self._last_analysis = {
            'difficulty_score': final_score,
            'difficulty_level': difficulty_level,
            'bpm_score': bpm_score,
            'frequency_variance_score': freq_variance_score,
            'beat_density_score': beat_density_score,
            'components': {
                'bpm': audio_features.get('tempo', {}).get('bpm', 120.0),
                'beat_count': audio_features.get('beats', {}).get('count', 0),
                'duration': audio_features.get('duration', 1.0),
                'spectral_variance': self._calculate_spectral_variance(audio_features)
            }
        }

        return self._last_analysis

    def analyze_difficulty_from_course(self, course) -> Dict:
        """
        Course 객체로부터 난이도 분석

        Args:
            course: Course 객체

        Returns:
            난이도 분석 결과
        """
        stats = course.get_statistics()

        # 장애물 밀도 기반 점수
        density = stats['density']
        density_score = self._normalize_value(
            density,
            self.BEAT_DENSITY_MIN,
            self.BEAT_DENSITY_MAX
        ) * 100.0

        # 장애물 타입 다양성
        type_diversity = len([v for v in stats['by_type'].values() if v > 0])
        diversity_score = (type_diversity / 3) * 100.0

        # 최종 점수 (밀도 70%, 다양성 30%)
        final_score = density_score * 0.7 + diversity_score * 0.3

        difficulty_level = self._determine_difficulty_level(final_score)

        return {
            'difficulty_score': final_score,
            'difficulty_level': difficulty_level,
            'density_score': density_score,
            'diversity_score': diversity_score,
            'components': {
                'obstacle_density': density,
                'total_obstacles': stats['total_obstacles'],
                'duration': stats['duration'],
                'type_diversity': type_diversity
            }
        }

    # ============================================================
    # Private Methods - 점수 계산
    # ============================================================

    def _calculate_bpm_score(self, features: Dict) -> float:
        """
        BPM 기반 점수 계산 (private)

        Args:
            features: 오디오 features

        Returns:
            BPM 점수 (0.0~100.0)
        """
        bpm = features.get('tempo', {}).get('bpm', 120.0)

        # BPM 정규화
        normalized_bpm = self._normalize_value(bpm, self.BPM_MIN, self.BPM_MAX)

        return normalized_bpm * 100.0

    def _calculate_frequency_variance_score(self, features: Dict) -> float:
        """
        주파수 분산 점수 계산 (private)

        Args:
            features: 오디오 features

        Returns:
            주파수 분산 점수 (0.0~100.0)
        """
        spectral_variance = self._calculate_spectral_variance(features)

        # 주파수 분산이 클수록 난이도 높음
        # 0~1 범위로 정규화
        normalized_variance = min(spectral_variance / 1000.0, 1.0)

        return normalized_variance * 100.0

    def _calculate_beat_density_score(self, features: Dict) -> float:
        """
        비트 밀도 점수 계산 (private)

        Args:
            features: 오디오 features

        Returns:
            비트 밀도 점수 (0.0~100.0)
        """
        beat_count = features.get('beats', {}).get('count', 0)
        duration = features.get('duration', 1.0)

        # 비트 밀도 (beats/second)
        beat_density = beat_count / duration if duration > 0 else 0

        # 정규화
        normalized_density = self._normalize_value(
            beat_density,
            self.BEAT_DENSITY_MIN,
            self.BEAT_DENSITY_MAX
        )

        return normalized_density * 100.0

    def _calculate_spectral_variance(self, features: Dict) -> float:
        """
        스펙트럼 분산 계산 (private)

        Args:
            features: 오디오 features

        Returns:
            스펙트럼 분산 값
        """
        spectral = features.get('spectral', {})

        # centroid와 rolloff가 dict 형태일 경우 'mean' 값 추출
        centroid = spectral.get('centroid', {})
        if isinstance(centroid, dict):
            centroid = centroid.get('mean', 0.0)

        rolloff = spectral.get('rolloff', {})
        if isinstance(rolloff, dict):
            rolloff = rolloff.get('mean', 0.0)

        # 간단한 분산 추정 (centroid와 rolloff 차이)
        variance = abs(rolloff - centroid)

        return variance

    def _normalize_value(self, value: float, min_val: float, max_val: float) -> float:
        """
        값을 0~1 범위로 정규화 (private)

        Args:
            value: 정규화할 값
            min_val: 최소값
            max_val: 최대값

        Returns:
            정규화된 값 (0.0~1.0)
        """
        if max_val == min_val:
            return 0.0

        normalized = (value - min_val) / (max_val - min_val)
        return max(0.0, min(1.0, normalized))

    def _determine_difficulty_level(self, score: float) -> str:
        """
        점수로부터 난이도 레벨 판정 (private)

        Args:
            score: 난이도 점수 (0~100)

        Returns:
            난이도 레벨 ('easy', 'normal', 'hard', 'expert')
        """
        if score < self.DIFFICULTY_THRESHOLDS['easy']:
            return 'easy'
        elif score < self.DIFFICULTY_THRESHOLDS['normal']:
            return 'normal'
        elif score < self.DIFFICULTY_THRESHOLDS['hard']:
            return 'hard'
        else:
            return 'expert'

    # ============================================================
    # Getters
    # ============================================================

    @property
    def last_analysis(self) -> Dict:
        """마지막 분석 결과 (읽기 전용)"""
        return self._last_analysis.copy()

    def get_difficulty_description(self, level: str) -> str:
        """
        난이도 레벨 설명 반환

        Args:
            level: 난이도 레벨

        Returns:
            설명 문자열
        """
        descriptions = {
            'easy': '초보자용 - 느린 템포, 단순한 패턴',
            'normal': '보통 - 적당한 속도와 복잡도',
            'hard': '어려움 - 빠른 템포, 복잡한 패턴',
            'expert': '전문가용 - 매우 빠른 템포, 고난이도 패턴'
        }

        return descriptions.get(level, '알 수 없음')
