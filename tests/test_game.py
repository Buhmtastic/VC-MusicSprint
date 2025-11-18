# -*- coding: utf-8 -*-
"""
Phase 3 Tests: 캐릭터 및 자동 플레이 시스템

테스트 범위:
- Character 클래스 (물리, 상태 전환)
- AutoPlayController (Strategy Pattern, AI 의사결정)
- Game 클래스 (게임 루프, 충돌 감지)
"""

import pytest
import sys
from pathlib import Path
import numpy as np

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.game.character import Character, CharacterState
from src.game.auto_play_controller import AutoPlayController, Action
from src.game.game import Game, GameState
from src.course.course import Course
from src.course.obstacle import BeatObstacle, FrequencyWall, AmplitudeGap


# ============================================================================
# Character Tests
# ============================================================================

class TestCharacter:
    """Character 클래스 테스트"""

    def test_character_initialization(self):
        """캐릭터 초기화 테스트"""
        char = Character(x=100.0)

        assert char.x == 100.0
        assert char.y == Character.GROUND_Y
        assert char.velocity_y == 0.0
        assert char.state == CharacterState.RUNNING

    def test_character_encapsulation(self):
        """캡슐화 테스트: private 속성 접근 불가"""
        char = Character()

        # Property로만 접근 가능
        assert hasattr(char, 'x')
        assert hasattr(char, 'y')

        # Private 속성 직접 수정 불가 (권장 사항)
        # 실제로는 접근 가능하지만 OOP 원칙상 금지
        assert hasattr(char, '_x')
        assert hasattr(char, '_y')

    def test_auto_jump(self):
        """자동 점프 테스트"""
        char = Character()

        # 점프 전 상태
        assert char.state == CharacterState.RUNNING

        # 점프 실행
        success = char.auto_jump()
        assert success is True
        assert char.state == CharacterState.JUMPING
        assert char.velocity_y < 0  # 위로 향하는 속도

    def test_jump_physics(self):
        """점프 물리 시뮬레이션 테스트"""
        char = Character()
        char.auto_jump()

        # 몇 프레임 업데이트
        for _ in range(10):
            char.update(1/60)  # 60 FPS

        # 중력에 의해 속도가 증가했는지 확인
        assert char.velocity_y > Character.JUMP_VELOCITY

    def test_landing_after_jump(self):
        """점프 후 착지 테스트"""
        char = Character()
        char.auto_jump()

        # 충분히 업데이트하여 착지할 때까지
        for _ in range(100):
            char.update(1/60)

        # 착지 확인
        assert char.state == CharacterState.RUNNING
        assert char.y == Character.GROUND_Y
        assert char.velocity_y == 0.0

    def test_auto_duck(self):
        """자동 숙이기 테스트"""
        char = Character()

        # 숙이기 실행
        success = char.auto_duck()
        assert success is True
        assert char.state == CharacterState.DUCKING

    def test_duck_recovery(self):
        """숙이기 후 복귀 테스트"""
        char = Character()
        char.auto_duck()

        # 충분히 업데이트
        for _ in range(60):  # 1초
            char.update(1/60)

        # 달리기로 복귀
        assert char.state == CharacterState.RUNNING

    def test_cannot_duck_while_jumping(self):
        """점프 중 숙이기 불가 테스트"""
        char = Character()
        char.auto_jump()

        # 점프 중에는 숙이기 불가
        success = char.auto_duck()
        assert success is False
        assert char.state == CharacterState.JUMPING

    def test_hitbox(self):
        """히트박스 반환 테스트"""
        char = Character()
        hitbox = char.get_hitbox()

        assert len(hitbox) == 4
        x, y, w, h = hitbox
        assert x == char.x
        assert y == char.y
        assert w == char.width
        assert h == char.height

    def test_get_info(self):
        """캐릭터 정보 반환 테스트"""
        char = Character()
        info = char.get_info()

        assert 'x' in info
        assert 'y' in info
        assert 'state' in info
        assert info['state'] == 'running'


# ============================================================================
# AutoPlayController Tests
# ============================================================================

class TestAutoPlayController:
    """AutoPlayController 클래스 테스트 (Strategy Pattern)"""

    def test_controller_initialization(self):
        """컨트롤러 초기화 테스트"""
        controller = AutoPlayController(difficulty=1.0)
        assert controller.difficulty == 1.0

    def test_decide_action_no_obstacles(self):
        """장애물 없을 때 행동 결정 테스트"""
        controller = AutoPlayController()
        char = Character()

        action = controller.decide_action(char, [], current_time=0.0)
        assert action == Action.NONE

    def test_decide_action_for_beat_obstacle(self):
        """BeatObstacle 회피 전략 테스트"""
        controller = AutoPlayController(difficulty=1.0)
        char = Character()

        # 비트 장애물 생성 (가까운 미래)
        beat_obs = BeatObstacle(time=0.25, x_position=100.0, beat_strength=0.8)
        obstacles = [beat_obs]

        action = controller.decide_action(
            char, obstacles, current_time=0.0
        )

        # 점프해야 함
        assert action == Action.JUMP

    def test_decide_action_for_high_frequency_wall(self):
        """높은 FrequencyWall 회피 전략 테스트 (숙이기)"""
        controller = AutoPlayController(difficulty=1.0)
        char = Character()

        # 높은 벽 생성 (높은 주파수 = 큰 벽)
        freq_wall = FrequencyWall(time=0.20, x_position=100.0, frequency=4500.0, max_frequency=5000.0)
        obstacles = [freq_wall]

        action = controller.decide_action(
            char, obstacles, current_time=0.0
        )

        # 숙이기 또는 점프 (높이에 따라)
        assert action in [Action.DUCK, Action.NONE]

    def test_decide_action_for_amplitude_gap(self):
        """AmplitudeGap 회피 전략 테스트"""
        controller = AutoPlayController(difficulty=1.0)
        char = Character()

        # 큰 간격 생성
        amp_gap = AmplitudeGap(time=0.25, x_position=100.0, amplitude=0.9)
        obstacles = [amp_gap]

        action = controller.decide_action(
            char, obstacles, current_time=0.0
        )

        # 점프해야 함
        assert action == Action.JUMP

    def test_execute_action_jump(self):
        """점프 실행 테스트"""
        controller = AutoPlayController()
        char = Character()

        success = controller.execute_action(Action.JUMP, char, current_time=0.0)
        assert success is True
        assert char.state == CharacterState.JUMPING

    def test_execute_action_duck(self):
        """숙이기 실행 테스트"""
        controller = AutoPlayController()
        char = Character()

        success = controller.execute_action(Action.DUCK, char, current_time=0.0)
        assert success is True
        assert char.state == CharacterState.DUCKING

    def test_cooldown_prevention(self):
        """중복 실행 방지 (쿨다운) 테스트"""
        controller = AutoPlayController()
        char = Character()

        # 첫 실행
        success1 = controller.execute_action(Action.JUMP, char, current_time=0.0)
        assert success1 is True

        # 착지 전 다시 실행 (쿨다운)
        success2 = controller.execute_action(Action.JUMP, char, current_time=0.05)
        assert success2 is False  # 쿨다운으로 실행 안 됨


# ============================================================================
# Game Tests
# ============================================================================

class TestGame:
    """Game 클래스 테스트"""

    def create_test_course(self) -> Course:
        """테스트용 코스 생성"""
        course = Course(duration=5.0, name="Test Course")

        # 몇 개 장애물 추가
        course.add_obstacle(BeatObstacle(time=1.0, x_position=100.0, beat_strength=0.8))
        course.add_obstacle(FrequencyWall(time=2.0, x_position=100.0, frequency=2000.0))
        course.add_obstacle(AmplitudeGap(time=3.0, x_position=100.0, amplitude=0.7))

        course.finalize()
        return course

    def test_game_initialization(self):
        """게임 초기화 테스트"""
        course = self.create_test_course()
        game = Game(course)

        assert game.state == GameState.NOT_STARTED
        assert game.current_time == 0.0
        assert game.score == 0

    def test_game_initialization_requires_finalized_course(self):
        """Finalize되지 않은 코스로 게임 시작 불가 테스트"""
        course = Course(duration=5.0)

        with pytest.raises(ValueError):
            game = Game(course)

    def test_game_start(self):
        """게임 시작 테스트"""
        course = self.create_test_course()
        game = Game(course)

        game.start()
        assert game.state == GameState.PLAYING

    def test_game_update(self):
        """게임 업데이트 테스트"""
        course = self.create_test_course()
        game = Game(course)

        game.start()

        # 몇 프레임 업데이트
        for _ in range(10):
            continues = game.update(1/60)
            assert continues is True

        # 시간이 흘렀는지 확인
        assert game.current_time > 0.0

    def test_game_auto_finish(self):
        """음악 종료 시 게임 자동 종료 테스트"""
        course = self.create_test_course()
        game = Game(course)

        game.start()

        # 코스 길이보다 긴 시간 업데이트
        for _ in range(600):  # 10초 (코스는 5초)
            continues = game.update(1/60)
            if not continues:
                break

        # 게임 종료 확인
        assert game.state == GameState.FINISHED
        assert game.current_time >= course.duration

    def test_game_pause_resume(self):
        """게임 일시정지/재개 테스트"""
        course = self.create_test_course()
        game = Game(course)

        game.start()
        assert game.state == GameState.PLAYING

        game.pause()
        assert game.state == GameState.PAUSED

        game.resume()
        assert game.state == GameState.PLAYING

    def test_get_statistics(self):
        """통계 정보 반환 테스트"""
        course = self.create_test_course()
        game = Game(course)

        game.start()
        stats = game.get_statistics()

        assert 'score' in stats
        assert 'current_time' in stats
        assert 'obstacles_avoided' in stats
        assert 'obstacles_hit' in stats
        assert 'success_rate' in stats

    def test_active_obstacles_update(self):
        """활성 장애물 업데이트 테스트"""
        course = self.create_test_course()
        game = Game(course)

        game.start()

        # 초기에는 활성 장애물이 있을 수 있음
        initial_count = len(game.active_obstacles)

        # 시간 진행
        for _ in range(60):  # 1초
            game.update(1/60)

        # 활성 장애물 수가 변했을 수 있음
        # (정확한 수는 타이밍에 따라 다름)
        assert isinstance(game.active_obstacles, list)

    def test_waveform_slice(self):
        """파형 슬라이스 반환 테스트"""
        course = self.create_test_course()

        # 더미 파형 생성
        waveform = np.sin(2 * np.pi * 440 * np.linspace(0, 5, 22050 * 5))
        game = Game(course, waveform=waveform, sample_rate=22050)

        game.start()

        # 파형 슬라이스 가져오기
        slice_data = game.get_waveform_slice(window_duration=1.0)
        assert slice_data is not None
        assert len(slice_data) > 0


# ============================================================================
# Integration Tests
# ============================================================================

class TestIntegration:
    """통합 테스트"""

    def test_full_game_simulation(self):
        """전체 게임 시뮬레이션 (통합 테스트)"""
        # 코스 생성
        course = Course(duration=3.0, name="Integration Test Course")
        course.add_obstacle(BeatObstacle(time=0.5, x_position=100.0, beat_strength=0.8))
        course.add_obstacle(BeatObstacle(time=1.0, x_position=100.0, beat_strength=0.9))
        course.add_obstacle(FrequencyWall(time=1.5, x_position=100.0, frequency=3000.0))
        course.add_obstacle(AmplitudeGap(time=2.0, x_position=100.0, amplitude=0.8))
        course.finalize()

        # 게임 시작
        game = Game(course)
        game.start()

        # 게임 루프 시뮬레이션
        frame_count = 0
        max_frames = 300  # 5초 (60 FPS)

        while frame_count < max_frames:
            continues = game.update(1/60)
            frame_count += 1

            if not continues:
                break

        # 게임이 정상 종료되었는지 확인
        assert game.state == GameState.FINISHED

        # 통계 확인
        stats = game.get_statistics()
        assert stats['obstacles_avoided'] + stats['obstacles_hit'] > 0

    def test_character_and_controller_integration(self):
        """캐릭터와 컨트롤러 통합 테스트"""
        char = Character()
        controller = AutoPlayController(difficulty=1.5)

        # 장애물 생성
        obstacle = BeatObstacle(time=0.25, x_position=100.0, beat_strength=0.8)

        # AI 의사결정
        action = controller.decide_action(char, [obstacle], current_time=0.0)

        # 행동 실행
        success = controller.execute_action(action, char, current_time=0.0)

        # 결과 확인
        if action != Action.NONE:
            assert success is True
            assert char.state != CharacterState.RUNNING


# ============================================================================
# Run Tests
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
