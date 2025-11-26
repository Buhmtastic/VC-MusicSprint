"""
Music Sprint - MVP Application
전체 파이프라인: 음악 선택 → 분석 → 게임 플레이 → 결과

Phase 5: MVP 완성
- 실제 음악 파일 지원
- 전체 파이프라인 통합
- 향상된 결과 화면
"""

import sys
import pygame
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.audio.audio_loader import AudioLoader, AudioLoadError
from src.audio.audio_analyzer import AudioAnalyzer
from src.course.course_generator import CourseGenerator
from src.game.game import Game, GameState
from src.game.renderer import GameRenderer
from src.ui.file_dialog import FileDialog, LoadingScreen
from src.ui.result_screen import ResultScreen


class MusicSprintApp:
    """
    Music Sprint MVP 애플리케이션

    책임:
    - 전체 워크플로우 조율 (UI → Audio → Course → Game → Results)
    - 사용자와의 상호작용 관리
    """

    def __init__(self):
        """애플리케이션 초기화"""
        self.file_dialog = FileDialog()
        self.audio_loader = AudioLoader()
        self.audio_analyzer = AudioAnalyzer()
        self.course_generator = CourseGenerator()
        self.loading_screen = LoadingScreen()
        self.result_screen = ResultScreen()

    def run(self) -> None:
        """
        메인 실행 함수
        """
        print("\n" + "="*60)
        print("  🎵 Music Sprint - MVP")
        print("  Music-Driven Idle Runner Game")
        print("="*60 + "\n")

        # ============================================================
        # Step 1: 파일 선택
        # ============================================================
        print("1️⃣  Select a music file...")
        file_path = self.file_dialog.select_audio_file()

        if not file_path:
            print("❌ File selection cancelled.")
            return

        print(f"✅ Selected: {Path(file_path).name}\n")

        # ============================================================
        # Step 2: 오디오 로드 및 분석
        # ============================================================
        try:
            self.loading_screen.show("🔄 Loading audio file...")
            waveform, sample_rate = self.audio_loader.load(file_path)
            self.loading_screen.hide()
            print(f"✅ Audio loaded!")
            print(f"   - Sample rate: {sample_rate} Hz")
            print(f"   - Duration: {len(waveform) / sample_rate:.1f}s\n")

        except AudioLoadError as e:
            self.loading_screen.hide()
            print(f"❌ Failed to load audio:\n{e}")
            return

        try:
            self.loading_screen.show("🔬 Analyzing audio features...")
            features = self.audio_analyzer.analyze(waveform, sample_rate)
            self.loading_screen.hide()
            print("✅ Analysis complete!\n")

        except Exception as e:
            self.loading_screen.hide()
            print(f"❌ Analysis failed:\n{e}")
            return

        # 분석 결과 출력
        self._print_audio_info(features, file_path)

        # ============================================================
        # Step 3: 코스 생성
        # ============================================================
        print("\n2️⃣  Generating course...")
        try:
            course = self.course_generator.generate(features)
            print(f"✅ Course generated!")
            print(f"   - Total obstacles: {course.obstacle_count}")
            print(f"   - Difficulty: {features['difficulty']['level']}")
            print(f"   - Density: {course.obstacle_count / course.duration:.1f} obs/s\n")

        except Exception as e:
            print(f"❌ Course generation failed:\n{e}")
            return

        # ============================================================
        # Step 4: 게임 실행
        # ============================================================
        print("3️⃣  Starting game...")
        print("   Controls: SPACE = Start, ESC = Exit\n")

        try:
            game_stats, score_info = self._run_game(course, waveform, sample_rate)

            if game_stats is None:
                print("⏭️  Game was cancelled.")
                return

        except Exception as e:
            print(f"❌ Game error:\n{e}")
            import traceback
            traceback.print_exc()
            return

        # ============================================================
        # Step 5: 결과 화면
        # ============================================================
        print("\n4️⃣  Displaying results...")

        try:
            # 파일명 기반 song_id 생성
            song_id = Path(file_path).stem

            # 하이스코어 로드
            from src.score.score_manager import ScoreManager
            score_manager = ScoreManager()
            high_score_data = score_manager.get_high_score(song_id)

            # 결과 화면 생성 및 저장
            result_filename = f"result_{song_id}.png"
            result_path = self.result_screen.display_and_save(
                game_stats=game_stats,
                score_info=score_info,
                high_score_data=high_score_data,
                filename=result_filename
            )

            print(f"✅ Result saved: {result_path}")

            # 하이스코어 저장
            score_manager.save_high_score(
                song_id=song_id,
                score=score_info['final_score'],
                difficulty_level=game_stats['difficulty_level'],
                stats=game_stats
            )

        except Exception as e:
            print(f"⚠️  Failed to save results: {e}")

        # ============================================================
        # Step 6: 종료
        # ============================================================
        print("\n" + "="*60)
        print("  🏁 Game Complete!")
        print("="*60)
        print(f"\n  Final Score: {score_info['final_score']:,}")
        print(f"  Difficulty:  {game_stats['difficulty_level'].upper()}")
        print(f"  Success:     {game_stats['success_rate']:.1f}%")
        print(f"  Max Combo:   {game_stats['max_combo']}")
        print("\n" + "="*60 + "\n")

        print("Close the result window to exit...")
        input("Press ENTER to continue...")

        self.result_screen.close()

    def _print_audio_info(self, features: dict, file_path: str) -> None:
        """
        오디오 분석 정보 출력

        Args:
            features: 분석 특징 딕셔너리
            file_path: 파일 경로
        """
        print("─" * 60)
        print("  📊 Audio Analysis")
        print("─" * 60)
        print(f"  📁 File:      {Path(file_path).name}")
        print(f"  ⏱️  Duration:  {features['duration']:.1f}s")
        print(f"  🎵 Tempo:     {features['tempo']['bpm']:.1f} BPM")
        print(f"  🥁 Beats:     {features['beats']['count']}")
        print(f"  🎮 Difficulty: {features['difficulty']['level']} ({features['difficulty']['score']:.1f}/100)")
        print("─" * 60)

    def _run_game(self, course, waveform, sample_rate):
        """
        게임 실행

        Args:
            course: Course 객체
            waveform: 오디오 파형
            sample_rate: 샘플레이트

        Returns:
            (game_stats, score_info) 또는 (None, None)
        """
        # 게임 초기화
        game = Game(course, waveform, sample_rate)
        renderer = GameRenderer(game)

        # 시작 화면
        waiting_for_start = True
        while waiting_for_start:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    renderer.cleanup()
                    return None, None
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        renderer.cleanup()
                        return None, None
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
                break

            clock.tick(60)

        # 게임 통계 수집
        game_stats = game.get_statistics()
        stats_summary = game.statistics_tracker.get_summary()

        # 최종 점수 계산
        score_info = game.score_manager.calculate_final_score(
            obstacles_avoided=stats_summary['obstacles_avoided'],
            perfect_dodges=game_stats['perfect_dodges'],
            max_combo=stats_summary['max_combo'],
            accuracy=stats_summary['timing_accuracy'],
            difficulty_level=game.difficulty_level
        )

        # 정리
        renderer.cleanup()

        return game_stats, score_info


def main():
    """메인 진입점"""
    try:
        app = MusicSprintApp()
        app.run()

        print("\n  👋 Thank you for playing Music Sprint!")
        print("="*60 + "\n")

    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user.")
    except Exception as e:
        print(f"\n\n❌ Unexpected error:\n{e}")
        import traceback
        traceback.print_exc()
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
