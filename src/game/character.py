# -*- coding: utf-8 -*-
"""
Character Class
자동으로 달리고 장애물을 회피하는 캐릭터

책임:
- 캐릭터 위치 및 속도 관리 (캡슐화)
- 자동 점프 및 숙이기 동작
- 물리 시뮬레이션 (중력, 속도)
- 상태 전환 (달리기/점프/숙이기)
"""

from enum import Enum
from typing import Tuple


class CharacterState(Enum):
    """캐릭터 상태"""
    RUNNING = "running"
    JUMPING = "jumping"
    DUCKING = "ducking"


class Character:
    """
    자동 플레이 캐릭터 클래스

    OOP 원칙:
    - 캡슐화: 모든 속성은 private (_prefix)
    - 단일 책임: 캐릭터의 물리/상태만 관리
    - 정보 은닉: getter로만 상태 접근 가능
    """

    # 물리 상수
    GRAVITY = 980.0  # pixels/s^2 (지구 중력)
    JUMP_VELOCITY = -400.0  # pixels/s (위로 점프)
    GROUND_Y = 400.0  # 지면 Y 좌표
    RUNNING_Y = GROUND_Y  # 달릴 때 Y 위치
    DUCKING_Y = GROUND_Y + 20.0  # 숙일 때 Y 위치 (약간 낮춤)

    # 캐릭터 크기
    WIDTH = 40.0
    HEIGHT = 60.0
    DUCKING_HEIGHT = 30.0  # 숙일 때 높이

    # 자동 플레이 타이밍
    JUMP_DURATION = 0.8  # 점프 지속 시간 (초)
    DUCK_DURATION = 0.5  # 숙이기 지속 시간 (초)

    def __init__(self, x: float = 100.0, y: float = None):
        """
        캐릭터 초기화

        Args:
            x: 초기 X 위치 (기본: 100)
            y: 초기 Y 위치 (기본: GROUND_Y)
        """
        # Private 속성 - 외부 접근 불가
        self._x = x
        self._y = y if y is not None else self.GROUND_Y
        self._velocity_y = 0.0  # Y 방향 속도
        self._state = CharacterState.RUNNING

        # 동작 타이머
        self._jump_timer = 0.0
        self._duck_timer = 0.0

    # ============================================================
    # Public Methods - 외부 인터페이스
    # ============================================================

    def update(self, delta_time: float) -> None:
        """
        캐릭터 상태 업데이트 (매 프레임 호출)

        Args:
            delta_time: 이전 프레임으로부터 경과 시간 (초)
        """
        # 타이머 업데이트
        if self._jump_timer > 0:
            self._jump_timer -= delta_time
        if self._duck_timer > 0:
            self._duck_timer -= delta_time

        # 상태별 물리 처리
        if self._state == CharacterState.JUMPING:
            self._update_jump_physics(delta_time)
        elif self._state == CharacterState.DUCKING:
            self._update_duck_state()
        else:  # RUNNING
            self._update_running_state()

    def auto_jump(self) -> bool:
        """
        자동 점프 실행 (비트 장애물 회피용)

        Returns:
            점프 성공 여부 (이미 점프 중이면 False)
        """
        # 지면에 있을 때만 점프 가능
        if self._state != CharacterState.RUNNING:
            return False

        self._state = CharacterState.JUMPING
        self._velocity_y = self.JUMP_VELOCITY
        self._jump_timer = self.JUMP_DURATION
        return True

    def auto_duck(self) -> bool:
        """
        자동 숙이기 실행 (주파수 벽 회피용)

        Returns:
            숙이기 성공 여부
        """
        # 점프 중이 아닐 때만 숙이기 가능
        if self._state == CharacterState.JUMPING:
            return False

        self._state = CharacterState.DUCKING
        self._duck_timer = self.DUCK_DURATION
        return True

    # ============================================================
    # Getters - 읽기 전용 접근
    # ============================================================

    @property
    def x(self) -> float:
        """X 좌표 (읽기 전용)"""
        return self._x

    @property
    def y(self) -> float:
        """Y 좌표 (읽기 전용)"""
        return self._y

    @property
    def velocity_y(self) -> float:
        """Y 방향 속도 (읽기 전용)"""
        return self._velocity_y

    @property
    def state(self) -> CharacterState:
        """현재 상태 (읽기 전용)"""
        return self._state

    @property
    def width(self) -> float:
        """캐릭터 너비 (충돌 감지용)"""
        return self.WIDTH

    @property
    def height(self) -> float:
        """캐릭터 높이 (상태에 따라 변함)"""
        if self._state == CharacterState.DUCKING:
            return self.DUCKING_HEIGHT
        return self.HEIGHT

    def get_hitbox(self) -> Tuple[float, float, float, float]:
        """
        충돌 감지용 히트박스 반환

        Returns:
            (x, y, width, height) 튜플
        """
        return (self._x, self._y, self.width, self.height)

    def get_info(self) -> dict:
        """
        디버깅/로깅용 캐릭터 정보

        Returns:
            캐릭터 상태 정보 딕셔너리
        """
        return {
            'x': self._x,
            'y': self._y,
            'velocity_y': self._velocity_y,
            'state': self._state.value,
            'width': self.width,
            'height': self.height,
            'on_ground': self._is_on_ground()
        }

    # ============================================================
    # Private Methods - 내부 구현
    # ============================================================

    def _update_jump_physics(self, delta_time: float) -> None:
        """
        점프 물리 시뮬레이션 (private)

        Args:
            delta_time: 델타 타임 (초)
        """
        # 중력 적용
        self._velocity_y += self.GRAVITY * delta_time

        # 위치 업데이트
        self._y += self._velocity_y * delta_time

        # 지면 충돌 체크
        if self._y >= self.GROUND_Y:
            self._y = self.GROUND_Y
            self._velocity_y = 0.0
            self._state = CharacterState.RUNNING

    def _update_duck_state(self) -> None:
        """숙이기 상태 업데이트 (private)"""
        self._y = self.DUCKING_Y

        # 숙이기 타이머 종료 시 달리기로 전환
        if self._duck_timer <= 0:
            self._state = CharacterState.RUNNING

    def _update_running_state(self) -> None:
        """달리기 상태 업데이트 (private)"""
        self._y = self.RUNNING_Y
        self._velocity_y = 0.0

    def _is_on_ground(self) -> bool:
        """지면에 있는지 확인 (private)"""
        return abs(self._y - self.GROUND_Y) < 1.0
