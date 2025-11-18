"""
Music Sprint - Phase 1 프로토타입
음원 분석 데모 프로그램
"""

import sys
import json
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.audio.audio_loader import AudioLoader, AudioLoadError
from src.audio.audio_analyzer import AudioAnalyzer
from src.ui.file_dialog import FileDialog, LoadingScreen


class MusicSprintDemo:
    """
    Music Sprint Phase 1 데모 애플리케이션

    책임:
    - 전체 워크플로우 조율 (UI → Loader → Analyzer)
    - 사용자와의 상호작용 관리
    """

    def __init__(self):
        """데모 앱 초기화"""
        self.file_dialog = FileDialog()
        self.audio_loader = AudioLoader()
        self.audio_analyzer = AudioAnalyzer()
        self.loading_screen = LoadingScreen()

    def run(self) -> None:
        """
        메인 실행 함수
        """
        print("\n" + "="*60)
        print("  🎵 Music Sprint - Phase 1 프로토타입")
        print("  음원 파형 분석 데모")
        print("="*60 + "\n")

        # 1. 파일 선택
        print("1️⃣  음악 파일을 선택해주세요...")
        file_path = self.file_dialog.select_audio_file()

        if not file_path:
            print("❌ 파일 선택이 취소되었습니다.")
            return

        print(f"✅ 선택된 파일: {Path(file_path).name}\n")

        # 2. 파일 로드
        try:
            self.loading_screen.show("🔄 오디오 파일 로딩 중...")
            waveform, sample_rate = self.audio_loader.load(file_path)
            self.loading_screen.hide()
            print(f"✅ 파일 로드 성공!")
            print(f"   - 샘플 레이트: {sample_rate} Hz")
            print(f"   - 파형 길이: {len(waveform)} samples\n")

        except AudioLoadError as e:
            self.loading_screen.hide()
            print(f"❌ 오디오 로드 실패:\n{e}")
            return

        # 3. 파형 분석
        try:
            self.loading_screen.show("🔬 음원 분석 중...")
            features = self.audio_analyzer.analyze(waveform, sample_rate)
            self.loading_screen.hide()
            print("✅ 분석 완료!\n")

        except Exception as e:
            self.loading_screen.hide()
            print(f"❌ 분석 실패:\n{e}")
            return

        # 4. 결과 출력
        self._print_analysis_results(features, file_path)

        # 5. 결과 저장 옵션
        self._save_results_option(features, file_path)

    def _print_analysis_results(self, features: dict, file_path: str) -> None:
        """
        분석 결과를 콘솔에 출력

        Args:
            features: 분석 특징 딕셔너리
            file_path: 파일 경로
        """
        print("\n" + "="*60)
        print("  📊 음원 분석 결과")
        print("="*60 + "\n")

        print(f"📁 파일명: {Path(file_path).name}")
        print(f"⏱️  총 길이: {features['duration']:.2f}초")
        print(f"🎵 템포: {features['tempo']['bpm']:.1f} BPM")
        print(f"🥁 비트 개수: {features['beats']['count']}개")
        print(f"📈 평균 볼륨: {features['amplitude']['mean']:.4f}")
        print(f"📊 최대 볼륨: {features['amplitude']['max']:.4f}")
        print(f"🎚️  볼륨 변화: {features['difficulty']['amplitude_variation']:.4f}")
        print(f"🎼 주파수 복잡도: {features['spectral']['centroid']['mean']:.1f} Hz")

        print(f"\n{'='*60}")
        print(f"  🎮 게임 난이도 분석")
        print(f"{'='*60}\n")

        difficulty = features['difficulty']
        print(f"🏆 난이도 등급: {difficulty['level']}")
        print(f"📊 난이도 점수: {difficulty['score']:.1f}/100")
        print(f"   - 비트 밀도: {difficulty['beat_density']:.1f} beats/min")
        print(f"   - 볼륨 변화: {difficulty['amplitude_variation']:.4f}")
        print(f"   - 주파수 복잡도: {difficulty['spectral_complexity']:.1f}")

        # 비트 타이밍 샘플 (처음 10개)
        print(f"\n{'='*60}")
        print(f"  🥁 비트 타이밍 (처음 10개)")
        print(f"{'='*60}\n")

        beat_times = features['beats']['times'][:10]
        for i, beat_time in enumerate(beat_times, 1):
            print(f"  비트 {i}: {beat_time:.3f}초")

        if len(features['beats']['times']) > 10:
            print(f"  ... (총 {features['beats']['count']}개)")

        print()

    def _save_results_option(self, features: dict, file_path: str) -> None:
        """
        결과 저장 옵션 제공

        Args:
            features: 분석 특징 딕셔너리
            file_path: 파일 경로
        """
        print("\n" + "="*60)
        response = input("📝 분석 결과를 JSON 파일로 저장하시겠습니까? (y/n): ")

        if response.lower() in ['y', 'yes']:
            # 결과 파일명 생성
            original_name = Path(file_path).stem
            output_path = Path("assets") / f"{original_name}_analysis.json"

            # assets 폴더가 없으면 생성
            output_path.parent.mkdir(exist_ok=True)

            # JSON으로 저장
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(features, f, indent=2, ensure_ascii=False)

            print(f"✅ 분석 결과 저장 완료: {output_path}")
        else:
            print("⏭️  저장 건너뛰기")


def main():
    """메인 진입점"""
    try:
        demo = MusicSprintDemo()
        demo.run()

        print("\n" + "="*60)
        print("  👋 Music Sprint Phase 1 데모를 종료합니다.")
        print("="*60 + "\n")

    except KeyboardInterrupt:
        print("\n\n⚠️  사용자에 의해 중단되었습니다.")
    except Exception as e:
        print(f"\n\n❌ 예상치 못한 오류 발생:\n{e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
