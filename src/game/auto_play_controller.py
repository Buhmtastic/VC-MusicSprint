# -*- coding: utf-8 -*-
"""
AutoPlayController Class
Strategy Pattern을 사용한 자동 플레이 의사결정

책임:
- 장애물 분석 및 회피 전략 결정
- 캐릭터 동작 지시 (점프/숙이기/대기)
- 타이밍 계산 및 예측
"""

from typing import Optional, List
from enum import Enum
from .character import Character
from ..course.obstacle import Obstacle, ObstacleType


class Action(Enum):
    """캐릭터가 취할 수 있는 행동"""
    NONE = "none"       # 아무것도 안 함
    JUMP = "jump"       # 점프
    DUCK = "duck"       # 숙이기


class AutoPlayController:
    """
    자동 플레이 컨트롤러 (Strategy Pattern)

    OOP 원칙:
    - Strategy Pattern: 장애물 타입에 따라 다른 전략 적용
    - 단일 책임: 의사결정만 담당 (실행은 Character가)
    - 캡슐화: 내부 판단 로직 숨김
    """

    # 타이밍 상수 (초)
    REACTION_TIME = 0.15  # 반응 시간 (150ms)
    JUMP_PREPARATION_TIME = 0.1  # 점프 준비 시간
    DUCK_PREPARATION_TIME = 0.05  # 숙이기 준비 시간

    # 안전 거리 (픽셀)
    SAFE_DISTANCE_HORIZONTAL = 50.0  # 수평 안전 거리

    def __init__(self, difficulty: float = 1.0):
        """
        AutoPlayController 초기화

        Args:
            difficulty: 난이도 계수 (0.0~2.0)
                       높을수록 더 정확하게 회피
        """
        self._difficulty = max(0.0, min(2.0, difficulty))
        self._last_action_time = -1.0  # 음수로 초기화하여 첫 행동 가능하게

    # ============================================================
    # Public Methods - 외부 인터페이스
    # ============================================================

    def decide_action(
        self,
        character: Character,
        upcoming_obstacles: List[Obstacle],
        current_time: float,
        game_speed: float = 300.0
    ) -> Action:
        """
        다가오는 장애물을 분석하여 행동 결정 (Strategy Pattern 핵심)

        Args:
            character: 캐릭터 객체
            upcoming_obstacles: 다가오는 장애물 리스트 (시간순 정렬)
            current_time: 현재 게임 시간 (초)
            game_speed: 게임 속도 (pixels/s)

        Returns:
            결정된 행동 (Action enum)
        """
        if not upcoming_obstacles:
            return Action.NONE

        # 가장 가까운 장애물 찾기
        nearest_obstacle = self._find_nearest_obstacle(
            upcoming_obstacles, current_time
        )

        if not nearest_obstacle:
            return Action.NONE

        # 타이밍 계산
        time_to_obstacle = nearest_obstacle.time - current_time

        # 너무 멀면 대기
        if time_to_obstacle > 2.0:
            return Action.NONE

        # 장애물 타입별 전략 적용
        action = self._select_strategy(
            nearest_obstacle,
            time_to_obstacle,
            character
        )

        return action

    def execute_action(
        self,
        action: Action,
        character: Character,
        current_time: float
    ) -> bool:
        """
        결정된 행동을 캐릭터에게 지시

        Args:
            action: 수행할 행동
            character: 캐릭터 객체
            current_time: 현재 시간

        Returns:
            실행 성공 여부
        """
        if action == Action.NONE:
            return True

        # 중복 실행 방지 (쿨다운)
        if current_time - self._last_action_time < 0.1:
            return False

        success = False
        if action == Action.JUMP:
            success = character.auto_jump()
        elif action == Action.DUCK:
            success = character.auto_duck()

        if success:
            self._last_action_time = current_time

        return success

    # ============================================================
    # Private Methods - Strategy 구현
    # ============================================================

    def _select_strategy(
        self,
        obstacle: Obstacle,
        time_to_obstacle: float,
        character: Character
    ) -> Action:
        """
        장애물 타입에 따라 적절한 전략 선택 (Strategy Pattern)

        Args:
            obstacle: 장애물 객체
            time_to_obstacle: 장애물까지 남은 시간
            character: 캐릭터 객체

        Returns:
            선택된 행동
        """
        obstacle_type = obstacle.get_type()

        # BeatObstacle → 점프
        if obstacle_type == ObstacleType.BEAT:
            return self._strategy_for_beat(obstacle, time_to_obstacle)

        # FrequencyWall → 높이에 따라 점프 또는 숙이기
        elif obstacle_type == ObstacleType.FREQUENCY:
            return self._strategy_for_frequency(obstacle, time_to_obstacle, character)

        # AmplitudeGap → 점프 (간격 뛰어넘기)
        elif obstacle_type == ObstacleType.AMPLITUDE:
            return self._strategy_for_amplitude(obstacle, time_to_obstacle)

        return Action.NONE

    def _strategy_for_beat(
        self,
        obstacle: Obstacle,
        time_to_obstacle: float
    ) -> Action:
        """
        BeatObstacle 회피 전략: 점프

        Args:
            obstacle: 비트 장애물
            time_to_obstacle: 남은 시간

        Returns:
            JUMP 또는 NONE
        """
        # 적절한 타이밍에 점프
        jump_timing = self.REACTION_TIME + self.JUMP_PREPARATION_TIME

        if abs(time_to_obstacle - jump_timing) < 0.1 * self._difficulty:
            return Action.JUMP

        return Action.NONE

    def _strategy_for_frequency(
        self,
        obstacle: Obstacle,
        time_to_obstacle: float,
        character: Character
    ) -> Action:
        """
        FrequencyWall 회피 전략: 높이에 따라 점프 또는 숙이기

        Args:
            obstacle: 주파수 벽
            time_to_obstacle: 남은 시간
            character: 캐릭터

        Returns:
            JUMP, DUCK, 또는 NONE
        """
        wall_height = obstacle.get_height()

        # 높은 벽 (80 이상) → 숙이기
        if wall_height >= 80:
            duck_timing = self.REACTION_TIME + self.DUCK_PREPARATION_TIME
            if abs(time_to_obstacle - duck_timing) < 0.1 * self._difficulty:
                return Action.DUCK

        # 중간 벽 (50~80) → 점프
        elif wall_height >= 50:
            jump_timing = self.REACTION_TIME + self.JUMP_PREPARATION_TIME
            if abs(time_to_obstacle - jump_timing) < 0.1 * self._difficulty:
                return Action.JUMP

        # 낮은 벽 (50 미만) → 아무것도 안 함 (그냥 통과)
        return Action.NONE

    def _strategy_for_amplitude(
        self,
        obstacle: Obstacle,
        time_to_obstacle: float
    ) -> Action:
        """
        AmplitudeGap 회피 전략: 점프로 간격 뛰어넘기

        Args:
            obstacle: 진폭 간격
            time_to_obstacle: 남은 시간

        Returns:
            JUMP 또는 NONE
        """
        gap_height = obstacle.get_height()

        # 큰 간격 (60 이상) → 점프 필요
        if gap_height >= 60:
            jump_timing = self.REACTION_TIME + self.JUMP_PREPARATION_TIME
            if abs(time_to_obstacle - jump_timing) < 0.15 * self._difficulty:
                return Action.JUMP

        # 작은 간격 → 통과 가능
        return Action.NONE

    def _find_nearest_obstacle(
        self,
        obstacles: List[Obstacle],
        current_time: float
    ) -> Optional[Obstacle]:
        """
        현재 시간 기준 가장 가까운 미래의 장애물 찾기

        Args:
            obstacles: 장애물 리스트
            current_time: 현재 시간

        Returns:
            가장 가까운 장애물 (없으면 None)
        """
        nearest = None
        min_distance = float('inf')

        for obstacle in obstacles:
            time_diff = obstacle.time - current_time

            # 이미 지나간 장애물 무시
            if time_diff < 0:
                continue

            # 너무 먼 장애물 무시 (2초 이상)
            if time_diff > 2.0:
                continue

            if time_diff < min_distance:
                min_distance = time_diff
                nearest = obstacle

        return nearest

    # ============================================================
    # Getters
    # ============================================================

    @property
    def difficulty(self) -> float:
        """난이도 계수 (읽기 전용)"""
        return self._difficulty

    def get_statistics(self) -> dict:
        """
        컨트롤러 통계 정보

        Returns:
            통계 딕셔너리
        """
        return {
            'difficulty': self._difficulty,
            'last_action_time': self._last_action_time,
            'reaction_time': self.REACTION_TIME
        }
