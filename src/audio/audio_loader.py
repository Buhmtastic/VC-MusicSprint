"""
AudioLoader 클래스
단일 책임 원칙: 오디오 파일 로딩만 담당
"""

import os
from pathlib import Path
from typing import Tuple, Optional
import librosa
import numpy as np


class AudioLoadError(Exception):
    """오디오 로드 중 발생하는 에러"""
    pass


class AudioLoader:
    """
    오디오 파일을 로드하는 클래스

    책임:
    - 로컬 파일 시스템에서 오디오 파일 로드
    - 파일 포맷 검증
    - 에러 처리 (손상된 파일, 지원하지 않는 포맷)

    지원 포맷: .mp3, .wav, .flac, .ogg
    """

    # 지원하는 오디오 파일 확장자
    SUPPORTED_FORMATS = {'.mp3', '.wav', '.flac', '.ogg'}

    # 기본 샘플링 레이트 (22050 Hz - librosa 기본값)
    DEFAULT_SAMPLE_RATE = 22050

    def __init__(self, sample_rate: int = DEFAULT_SAMPLE_RATE):
        """
        AudioLoader 초기화

        Args:
            sample_rate: 오디오 샘플링 레이트 (Hz)
        """
        self._sample_rate = sample_rate
        self._current_file_path: Optional[Path] = None

    def load(self, file_path: str) -> Tuple[np.ndarray, int]:
        """
        오디오 파일을 로드하여 파형 데이터와 샘플 레이트를 반환

        Args:
            file_path: 오디오 파일 경로

        Returns:
            (waveform, sample_rate): 파형 데이터와 샘플 레이트

        Raises:
            AudioLoadError: 파일 로드 실패 시
        """
        # 파일 경로 검증
        path = Path(file_path)
        self._validate_file(path)

        try:
            # librosa로 오디오 파일 로드
            # sr=None이면 원본 샘플 레이트 사용, sr=지정값이면 리샘플링
            waveform, sr = librosa.load(
                str(path),
                sr=self._sample_rate,
                mono=True  # 모노로 변환 (스테레오 → 모노)
            )

            self._current_file_path = path

            return waveform, sr

        except Exception as e:
            raise AudioLoadError(
                f"오디오 파일 로드 실패: {file_path}\n"
                f"에러: {str(e)}"
            )

    def _validate_file(self, path: Path) -> None:
        """
        파일 유효성 검증 (private 메서드)

        Args:
            path: 파일 경로

        Raises:
            AudioLoadError: 파일이 유효하지 않을 때
        """
        # 파일 존재 여부 확인
        if not path.exists():
            raise AudioLoadError(f"파일을 찾을 수 없습니다: {path}")

        # 파일인지 확인 (디렉토리 아님)
        if not path.is_file():
            raise AudioLoadError(f"디렉토리는 로드할 수 없습니다: {path}")

        # 파일 확장자 확인
        if path.suffix.lower() not in self.SUPPORTED_FORMATS:
            raise AudioLoadError(
                f"지원하지 않는 파일 포맷입니다: {path.suffix}\n"
                f"지원 포맷: {', '.join(self.SUPPORTED_FORMATS)}"
            )

        # 파일 크기 확인 (0바이트 파일 방지)
        if path.stat().st_size == 0:
            raise AudioLoadError(f"빈 파일입니다: {path}")

    @property
    def sample_rate(self) -> int:
        """샘플링 레이트 getter"""
        return self._sample_rate

    @property
    def current_file(self) -> Optional[str]:
        """현재 로드된 파일 경로"""
        return str(self._current_file_path) if self._current_file_path else None

    def get_file_info(self, file_path: str) -> dict:
        """
        파일을 로드하지 않고 메타데이터만 가져오기

        Args:
            file_path: 오디오 파일 경로

        Returns:
            파일 정보 딕셔너리 (duration, sample_rate, channels 등)
        """
        path = Path(file_path)
        self._validate_file(path)

        try:
            # 메타데이터만 로드 (파형 데이터는 로드하지 않음)
            duration = librosa.get_duration(path=str(path))

            return {
                'file_name': path.name,
                'file_path': str(path),
                'duration': duration,
                'file_size': path.stat().st_size,
                'format': path.suffix.lower()
            }
        except Exception as e:
            raise AudioLoadError(f"파일 정보 읽기 실패: {str(e)}")
