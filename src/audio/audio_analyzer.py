"""
AudioAnalyzer 클래스
음원 파형 분석 및 특징 추출
"""

from typing import Dict, List, Optional
import numpy as np
import librosa


class AudioAnalyzer:
    """
    음원 파형을 분석하여 게임에 필요한 특징을 추출하는 클래스

    책임:
    - FFT (Fast Fourier Transform) 분석
    - Beat Detection (비트 감지)
    - Amplitude Envelope (볼륨 변화)
    - Spectral Centroid (음색 분석)

    캡슐화: 모든 파형 데이터는 private 속성으로 관리
    """

    def __init__(self):
        """AudioAnalyzer 초기화"""
        # Private 속성들 (외부 직접 접근 불가)
        self._waveform: Optional[np.ndarray] = None
        self._sample_rate: Optional[int] = None
        self._features: Dict = {}

    def analyze(self, waveform: np.ndarray, sample_rate: int) -> Dict:
        """
        음원 파형을 분석하여 특징 추출

        Args:
            waveform: 오디오 파형 데이터 (numpy array)
            sample_rate: 샘플링 레이트

        Returns:
            분석 결과 딕셔너리
        """
        self._waveform = waveform
        self._sample_rate = sample_rate

        # 모든 특징 추출
        self._features = self._extract_features()

        return self._features

    def _extract_features(self) -> Dict:
        """
        모든 오디오 특징을 추출하는 private 메서드

        Returns:
            특징 딕셔너리
        """
        features = {}

        # 1. 기본 정보
        features['duration'] = len(self._waveform) / self._sample_rate
        features['sample_rate'] = self._sample_rate
        features['total_samples'] = len(self._waveform)

        # 2. Beat Detection (비트 감지)
        features['beats'] = self._detect_beats()

        # 3. Amplitude Envelope (볼륨 변화)
        features['amplitude'] = self._extract_amplitude_envelope()

        # 4. FFT 분석 (주파수 스펙트럼)
        features['spectral'] = self._extract_spectral_features()

        # 5. 템포 분석
        features['tempo'] = self._extract_tempo()

        # 6. 난이도 계산 (비트 밀도 기반)
        features['difficulty'] = self._calculate_difficulty(features)

        return features

    def _detect_beats(self) -> Dict:
        """
        비트 감지 (private 메서드)

        Returns:
            비트 정보 딕셔너리
        """
        # librosa의 beat tracker 사용
        tempo, beat_frames = librosa.beat.beat_track(
            y=self._waveform,
            sr=self._sample_rate
        )

        # 프레임 → 시간 변환
        beat_times = librosa.frames_to_time(
            beat_frames,
            sr=self._sample_rate
        )

        return {
            'count': len(beat_times),
            'times': beat_times.tolist(),  # numpy → list 변환
            'frames': beat_frames.tolist(),
            'tempo': tempo
        }

    def _extract_amplitude_envelope(self) -> Dict:
        """
        볼륨 변화 추출 (private 메서드)

        Returns:
            진폭 포락선 정보
        """
        # RMS (Root Mean Square) 에너지 계산
        rms = librosa.feature.rms(y=self._waveform)[0]

        # 시간축 생성
        times = librosa.frames_to_time(
            np.arange(len(rms)),
            sr=self._sample_rate
        )

        return {
            'rms': rms.tolist(),
            'times': times.tolist(),
            'mean': float(np.mean(rms)),
            'max': float(np.max(rms)),
            'min': float(np.min(rms))
        }

    def _extract_spectral_features(self) -> Dict:
        """
        주파수 스펙트럼 특징 추출 (private 메서드)

        Returns:
            스펙트럼 특징 딕셔너리
        """
        # Spectral Centroid (음색의 밝기)
        spectral_centroids = librosa.feature.spectral_centroid(
            y=self._waveform,
            sr=self._sample_rate
        )[0]

        # Spectral Rolloff (주파수 롤오프)
        spectral_rolloff = librosa.feature.spectral_rolloff(
            y=self._waveform,
            sr=self._sample_rate
        )[0]

        # Zero Crossing Rate (제로 크로싱 비율)
        zero_crossing = librosa.feature.zero_crossing_rate(
            self._waveform
        )[0]

        return {
            'centroid': {
                'values': spectral_centroids.tolist(),
                'mean': float(np.mean(spectral_centroids)),
                'std': float(np.std(spectral_centroids))
            },
            'rolloff': {
                'values': spectral_rolloff.tolist(),
                'mean': float(np.mean(spectral_rolloff))
            },
            'zero_crossing': {
                'values': zero_crossing.tolist(),
                'mean': float(np.mean(zero_crossing))
            }
        }

    def _extract_tempo(self) -> Dict:
        """
        템포 추출 (private 메서드)

        Returns:
            템포 정보
        """
        # 템포 추정
        tempo, _ = librosa.beat.beat_track(
            y=self._waveform,
            sr=self._sample_rate
        )

        # 템포 기반 난이도 계산
        # 느린 곡 (<80 BPM): Easy
        # 보통 곡 (80-140 BPM): Medium
        # 빠른 곡 (>140 BPM): Hard
        if tempo < 80:
            tempo_difficulty = 'Easy'
        elif tempo < 140:
            tempo_difficulty = 'Medium'
        else:
            tempo_difficulty = 'Hard'

        return {
            'bpm': float(tempo),
            'difficulty': tempo_difficulty
        }

    def _calculate_difficulty(self, features: Dict) -> Dict:
        """
        곡의 난이도 계산 (private 메서드)

        난이도 기준:
        - 비트 밀도 (beats per minute)
        - 볼륨 변화량 (amplitude variation)
        - 주파수 복잡도 (spectral complexity)

        Returns:
            난이도 정보
        """
        # 비트 밀도 (분당 비트 수)
        duration_minutes = features['duration'] / 60
        beat_density = features['beats']['count'] / duration_minutes if duration_minutes > 0 else 0

        # 볼륨 변화 표준편차
        amplitude_variation = np.std(features['amplitude']['rms'])

        # 주파수 복잡도 (spectral centroid의 표준편차)
        spectral_complexity = features['spectral']['centroid']['std']

        # 정규화된 난이도 점수 (0~100)
        # 가중치: 비트 밀도 40%, 볼륨 변화 30%, 주파수 복잡도 30%
        difficulty_score = (
            (min(beat_density / 2, 100) * 0.4) +
            (min(amplitude_variation * 1000, 100) * 0.3) +
            (min(spectral_complexity / 50, 100) * 0.3)
        )

        # 난이도 등급
        if difficulty_score < 30:
            difficulty_level = 'Easy'
        elif difficulty_score < 60:
            difficulty_level = 'Medium'
        elif difficulty_score < 80:
            difficulty_level = 'Hard'
        else:
            difficulty_level = 'Expert'

        return {
            'score': float(difficulty_score),
            'level': difficulty_level,
            'beat_density': float(beat_density),
            'amplitude_variation': float(amplitude_variation),
            'spectral_complexity': float(spectral_complexity)
        }

    def get_beats_at_time_range(self, start_time: float, end_time: float) -> List[float]:
        """
        특정 시간 범위의 비트 타이밍 반환

        Args:
            start_time: 시작 시간 (초)
            end_time: 종료 시간 (초)

        Returns:
            해당 범위의 비트 타이밍 리스트
        """
        if not self._features or 'beats' not in self._features:
            return []

        beat_times = self._features['beats']['times']
        return [t for t in beat_times if start_time <= t <= end_time]

    def get_summary(self) -> str:
        """
        분석 결과 요약 문자열 반환

        Returns:
            요약 문자열
        """
        if not self._features:
            return "분석되지 않음"

        return f"""
=== 음원 분석 결과 ===
총 길이: {self._features['duration']:.2f}초
템포: {self._features['tempo']['bpm']:.1f} BPM
비트 개수: {self._features['beats']['count']}개
평균 볼륨: {self._features['amplitude']['mean']:.4f}
난이도: {self._features['difficulty']['level']} ({self._features['difficulty']['score']:.1f}/100)
"""

    @property
    def features(self) -> Dict:
        """추출된 특징 반환 (읽기 전용)"""
        return self._features.copy()  # 복사본 반환 (원본 보호)

    @property
    def waveform(self) -> Optional[np.ndarray]:
        """파형 데이터 반환 (읽기 전용)"""
        return self._waveform.copy() if self._waveform is not None else None
