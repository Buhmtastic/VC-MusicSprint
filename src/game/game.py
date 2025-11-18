# -*- coding: utf-8 -*-
"""
Game Class
게임 메인 루프 및 음악 동기화

책임:
- 게임 루프 실행
- 음악 재생과 게임 타이밍 동기화
- 장애물 관리 및 충돌 감지
- 점수 계산 및 게임 상태 관리
"""

import time
from typing import Optional, List
from enum import Enum
import numpy as np

from .character import Character
from .auto_play_controller import AutoPlayController, Action
from ..course.course import Course
from ..course.obstacle import Obstacle


class GameState(Enum):
    """게임 상태"""
    NOT_STARTED = "not_started"
    PLAYING = "playing"
    PAUSED = "paused"
    FINISHED = "finished"


class CollisionResult:
    """충돌 감지 결과"""
    def __init__(self, collided: bool, obstacle: Optional[Obstacle] = None):
        self.collided = collided
        self.obstacle = obstacle


class Game:
    """
    게임 메인 클래스

    OOP 원칙:
    - 단일 책임: 게임 조율만 담당 (렌더링은 별도)
    - 의존성 주입: Course, Character, Controller를 외부에서 주입
    - 캡슐화: 게임 내부 상태 보호
    """

    # 게임 설정
    GAME_SPEED = 300.0  # 픽셀/초 (장애물이 다가오는 속도)
    TARGET_FPS = 60
    FRAME_TIME = 1.0 / TARGET_FPS

    # 충돌 허용 오차 (픽셀)
    COLLISION_TOLERANCE = 5.0

    # 점수 설정
    SCORE_PER_OBSTACLE_AVOIDED = 10
    SCORE_PERFECT_TIMING_BONUS = 5

    def __init__(
        self,
        course: Course,
        waveform: Optional[np.ndarray] = None,
        sample_rate: int = 22050
    ):
        """
        게임 초기화

        Args:
            course: 플레이할 코스
            waveform: 오디오 파형 (배경 렌더링용, 선택)
            sample_rate: 샘플레이트
        """
        if not course.is_finalized:
            raise ValueError("Course must be finalized before starting game")

        # 주입된 의존성
        self._course = course
        self._waveform = waveform
        self._sample_rate = sample_rate

        # 게임 객체 생성
        self._character = Character(x=100.0)
        self._controller = AutoPlayController(difficulty=1.0)

        # 게임 상태
        self._state = GameState.NOT_STARTED
        self._current_time = 0.0
        self._start_real_time = 0.0

        # 점수 및 통계
        self._score = 0
        self._obstacles_avoided = 0
        self._obstacles_hit = 0
        self._perfect_dodges = 0

        # 장애물 추적
        self._active_obstacles: List[Obstacle] = []
        self._passed_obstacles: List[Obstacle] = []

    # ============================================================
    # Public Methods - 게임 제어
    # ============================================================

    def start(self) -> None:
        """게임 시작"""
        if self._state != GameState.NOT_STARTED:
            raise RuntimeError("Game already started")

        self._state = GameState.PLAYING
        self._start_real_time = time.time()
        self._current_time = 0.0

    def update(self, delta_time: float) -> bool:
        """
        게임 상태 업데이트 (메인 루프에서 호출)

        Args:
            delta_time: 이전 프레임으로부터 경과 시간 (초)

        Returns:
            게임이 계속되면 True, 종료되면 False
        """
        if self._state != GameState.PLAYING:
            return False

        # 시간 업데이트
        self._current_time += delta_time

        # 음악 종료 체크
        if self._current_time >= self._course.duration:
            self._finish_game()
            return False

        # 캐릭터 업데이트
        self._character.update(delta_time)

        # 활성 장애물 업데이트
        self._update_active_obstacles()

        # 자동 플레이 AI 실행
        self._execute_auto_play()

        # 충돌 감지
        self._check_collisions()

        return True

    def pause(self) -> None:
        """게임 일시정지"""
        if self._state == GameState.PLAYING:
            self._state = GameState.PAUSED

    def resume(self) -> None:
        """게임 재개"""
        if self._state == GameState.PAUSED:
            self._state = GameState.PLAYING

    # ============================================================
    # Getters - 상태 조회
    # ============================================================

    @property
    def state(self) -> GameState:
        """현재 게임 상태"""
        return self._state

    @property
    def current_time(self) -> float:
        """현재 게임 시간 (초)"""
        return self._current_time

    @property
    def score(self) -> int:
        """현재 점수"""
        return self._score

    @property
    def character(self) -> Character:
        """캐릭터 객체 (렌더링용)"""
        return self._character

    @property
    def course(self) -> Course:
        """코스 객체"""
        return self._course

    @property
    def active_obstacles(self) -> List[Obstacle]:
        """현재 화면에 보이는 장애물 리스트"""
        return self._active_obstacles

    def get_statistics(self) -> dict:
        """
        게임 통계

        Returns:
            통계 정보 딕셔너리
        """
        total_obstacles = self._course.obstacle_count
        success_rate = 0.0
        if total_obstacles > 0:
            success_rate = (self._obstacles_avoided / total_obstacles) * 100.0

        return {
            'score': self._score,
            'current_time': self._current_time,
            'duration': self._course.duration,
            'progress': (self._current_time / self._course.duration) * 100.0,
            'obstacles_avoided': self._obstacles_avoided,
            'obstacles_hit': self._obstacles_hit,
            'perfect_dodges': self._perfect_dodges,
            'success_rate': success_rate,
            'state': self._state.value
        }

    def get_waveform_slice(self, window_duration: float = 2.0) -> Optional[np.ndarray]:
        """
        현재 시간 기준 파형 슬라이스 (배경 렌더링용)

        Args:
            window_duration: 표시할 파형 길이 (초)

        Returns:
            파형 데이터 (없으면 None)
        """
        if self._waveform is None:
            return None

        start_sample = int(self._current_time * self._sample_rate)
        end_sample = int((self._current_time + window_duration) * self._sample_rate)

        # 범위 체크
        if start_sample >= len(self._waveform):
            return None

        end_sample = min(end_sample, len(self._waveform))
        return self._waveform[start_sample:end_sample]

    # ============================================================
    # Private Methods - 내부 로직
    # ============================================================

    def _update_active_obstacles(self) -> None:
        """활성 장애물 리스트 업데이트"""
        # 현재 시간 기준 ±2초 범위의 장애물 가져오기
        time_window = 2.0
        self._active_obstacles = self._course.get_obstacles_in_range(
            self._current_time - 0.5,
            self._current_time + time_window
        )

    def _execute_auto_play(self) -> None:
        """자동 플레이 AI 실행"""
        # 다가오는 장애물 가져오기
        upcoming = [
            obs for obs in self._active_obstacles
            if obs.time > self._current_time
        ]

        # AI 의사결정
        action = self._controller.decide_action(
            self._character,
            upcoming,
            self._current_time,
            self.GAME_SPEED
        )

        # 행동 실행
        if action != Action.NONE:
            self._controller.execute_action(
                action,
                self._character,
                self._current_time
            )

    def _check_collisions(self) -> None:
        """충돌 감지 및 처리"""
        char_hitbox = self._character.get_hitbox()
        char_x, char_y, char_w, char_h = char_hitbox

        for obstacle in self._active_obstacles:
            # 이미 체크한 장애물 무시
            if obstacle in self._passed_obstacles:
                continue

            # 장애물이 캐릭터를 지나갔는지 확인
            if obstacle.time < self._current_time - 0.5:
                # 통과 성공
                self._on_obstacle_avoided(obstacle)
                self._passed_obstacles.append(obstacle)
                continue

            # 충돌 체크 (간단한 AABB 충돌)
            collision = self._detect_collision(obstacle, char_hitbox)

            if collision.collided:
                self._on_collision(obstacle)
                self._passed_obstacles.append(obstacle)

    def _detect_collision(
        self,
        obstacle: Obstacle,
        char_hitbox: tuple
    ) -> CollisionResult:
        """
        AABB 충돌 감지

        Args:
            obstacle: 장애물
            char_hitbox: 캐릭터 히트박스 (x, y, w, h)

        Returns:
            충돌 결과
        """
        char_x, char_y, char_w, char_h = char_hitbox

        # 장애물의 화면상 X 위치 계산
        time_diff = obstacle.time - self._current_time
        obstacle_x = char_x + time_diff * self.GAME_SPEED

        # 화면 밖이면 충돌 없음
        if obstacle_x < 0 or obstacle_x > 800:
            return CollisionResult(False)

        # AABB 충돌 감지 (허용 오차 포함)
        obs_height = obstacle.get_height()
        obs_y = self._character.GROUND_Y - obs_height
        obs_width = 20.0  # 장애물 너비 (임의 설정)

        # X축 충돌
        x_overlap = (
            char_x < obstacle_x + obs_width + self.COLLISION_TOLERANCE and
            char_x + char_w > obstacle_x - self.COLLISION_TOLERANCE
        )

        # Y축 충돌
        y_overlap = (
            char_y < obs_y + obs_height + self.COLLISION_TOLERANCE and
            char_y + char_h > obs_y - self.COLLISION_TOLERANCE
        )

        collided = x_overlap and y_overlap
        return CollisionResult(collided, obstacle if collided else None)

    def _on_obstacle_avoided(self, obstacle: Obstacle) -> None:
        """장애물 회피 성공 시 처리"""
        self._obstacles_avoided += 1
        self._score += self.SCORE_PER_OBSTACLE_AVOIDED

        # TODO: 완벽한 타이밍 판정 (나중에 구현)

    def _on_collision(self, obstacle: Obstacle) -> None:
        """충돌 발생 시 처리"""
        self._obstacles_hit += 1
        # NOTE: 현재는 충돌해도 게임이 계속됨 (이후 Phase에서 개선)

    def _finish_game(self) -> None:
        """게임 종료 처리"""
        self._state = GameState.FINISHED
        self._current_time = self._course.duration
