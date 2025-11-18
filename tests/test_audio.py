"""
Audio 모듈 테스트
"""

import pytest
import numpy as np
from pathlib import Path
import sys

# 프로젝트 루트를 경로에 추가
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.audio.audio_loader import AudioLoader, AudioLoadError
from src.audio.audio_analyzer import AudioAnalyzer


class TestAudioLoader:
    """AudioLoader 클래스 테스트"""

    def test_init(self):
        """초기화 테스트"""
        loader = AudioLoader()
        assert loader.sample_rate == AudioLoader.DEFAULT_SAMPLE_RATE
        assert loader.current_file is None

    def test_unsupported_format(self):
        """지원하지 않는 포맷 테스트"""
        loader = AudioLoader()

        # 더미 파일 생성
        dummy_file = Path("test.txt")
        dummy_file.write_text("dummy")

        with pytest.raises(AudioLoadError) as exc_info:
            loader.load(str(dummy_file))

        assert "지원하지 않는 파일 포맷" in str(exc_info.value)

        # 정리
        dummy_file.unlink()

    def test_file_not_found(self):
        """존재하지 않는 파일 테스트"""
        loader = AudioLoader()

        with pytest.raises(AudioLoadError) as exc_info:
            loader.load("nonexistent_file.mp3")

        assert "파일을 찾을 수 없습니다" in str(exc_info.value)


class TestAudioAnalyzer:
    """AudioAnalyzer 클래스 테스트"""

    def test_init(self):
        """초기화 테스트"""
        analyzer = AudioAnalyzer()
        assert analyzer.waveform is None
        assert analyzer.features == {}

    def test_analyze_with_dummy_data(self):
        """더미 데이터로 분석 테스트"""
        analyzer = AudioAnalyzer()

        # 1초짜리 440Hz 사인파 생성 (A4 음)
        sample_rate = 22050
        duration = 1.0
        frequency = 440.0

        t = np.linspace(0, duration, int(sample_rate * duration))
        waveform = np.sin(2 * np.pi * frequency * t)

        # 분석 실행
        features = analyzer.analyze(waveform, sample_rate)

        # 기본 특징 확인
        assert 'duration' in features
        assert 'beats' in features
        assert 'amplitude' in features
        assert 'spectral' in features
        assert 'tempo' in features
        assert 'difficulty' in features

        # 길이 확인 (약 1초)
        assert abs(features['duration'] - 1.0) < 0.1

    def test_features_property(self):
        """features 프로퍼티 테스트 (복사본 반환 확인)"""
        analyzer = AudioAnalyzer()

        # 더미 데이터 분석
        waveform = np.random.randn(22050)
        features = analyzer.analyze(waveform, 22050)

        # features 프로퍼티로 가져오기
        features_copy = analyzer.features

        # 복사본인지 확인 (원본 수정해도 영향 없어야 함)
        features_copy['test'] = 'modified'
        assert 'test' not in analyzer.features


def test_integration():
    """통합 테스트 (더미 오디오 파일 생성 및 전체 파이프라인)"""
    # 더미 WAV 파일 생성
    import soundfile as sf

    sample_rate = 22050
    duration = 2.0
    frequency = 440.0

    t = np.linspace(0, duration, int(sample_rate * duration))
    waveform = np.sin(2 * np.pi * frequency * t)

    # 임시 파일 저장
    temp_file = Path("tests/temp_test.wav")
    temp_file.parent.mkdir(exist_ok=True)
    sf.write(str(temp_file), waveform, sample_rate)

    try:
        # 1. 로드
        loader = AudioLoader()
        loaded_waveform, loaded_sr = loader.load(str(temp_file))

        assert loaded_waveform is not None
        assert loaded_sr == sample_rate

        # 2. 분석
        analyzer = AudioAnalyzer()
        features = analyzer.analyze(loaded_waveform, loaded_sr)

        assert features['duration'] > 0
        assert features['beats']['count'] > 0
        assert features['difficulty']['level'] in ['Easy', 'Medium', 'Hard', 'Expert']

        print("\n✅ 통합 테스트 성공!")
        print(f"   - 길이: {features['duration']:.2f}초")
        print(f"   - 비트: {features['beats']['count']}개")
        print(f"   - 난이도: {features['difficulty']['level']}")

    finally:
        # 정리
        if temp_file.exists():
            temp_file.unlink()


if __name__ == "__main__":
    # pytest 없이 직접 실행 시
    print("🧪 통합 테스트 실행...\n")
    test_integration()
