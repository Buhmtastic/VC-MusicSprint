# -*- coding: utf-8 -*-
"""
StatisticsTracker Class
게임 플레이 통계 추적

책임:
- 점프/숙이기 통계 수집
- 콤보 추적 및 최대 콤보 기록
- 정확도 계산
- 통계 요약 제공
"""

from typing import Dict, List
from collections import deque


class StatisticsTracker:
    """
    통계 추적 클래스

    OOP 원칙:
    - 단일 책임: 통계 수집 및 계산만 담당
    - 캡슐화: 내부 통계 데이터 보호
    - 정보 제공: get_summary()로 읽기 전용 접근
    """

    def __init__(self):
        """StatisticsTracker 초기화"""
        # 행동 통계
        self._total_jumps = 0
        self._total_ducks = 0
        self._perfect_jumps = 0
        self._perfect_ducks = 0

        # 콤보 통계
        self._current_combo = 0
        self._max_combo = 0
        self._combo_history: List[int] = []

        # 장애물 통계
        self._obstacles_avoided = 0
        self._obstacles_hit = 0

        # 타이밍 정확도 (최근 20개 행동)
        self._timing_accuracy_buffer = deque(maxlen=20)

        # 시간 통계
        self._game_duration = 0.0
        self._play_start_time = 0.0

    # ============================================================
    # Public Methods - 데이터 수집
    # ============================================================

    def track_jump(self, is_perfect: bool = False, timing_accuracy: float = 1.0) -> None:
        """
        점프 행동 추적

        Args:
            is_perfect: 완벽한 타이밍 여부
            timing_accuracy: 타이밍 정확도 (0.0~1.0)
        """
        self._total_jumps += 1

        if is_perfect:
            self._perfect_jumps += 1

        self._timing_accuracy_buffer.append(timing_accuracy)

    def track_duck(self, is_perfect: bool = False, timing_accuracy: float = 1.0) -> None:
        """
        숙이기 행동 추적

        Args:
            is_perfect: 완벽한 타이밍 여부
            timing_accuracy: 타이밍 정확도 (0.0~1.0)
        """
        self._total_ducks += 1

        if is_perfect:
            self._perfect_ducks += 1

        self._timing_accuracy_buffer.append(timing_accuracy)

    def track_obstacle_avoided(self) -> None:
        """장애물 회피 성공 기록"""
        self._obstacles_avoided += 1
        self._increment_combo()

    def track_obstacle_hit(self) -> None:
        """장애물 충돌 기록"""
        self._obstacles_hit += 1
        self._reset_combo()

    def track_combo(self, combo_count: int) -> None:
        """
        현재 콤보 추적 (외부에서 직접 설정)

        Args:
            combo_count: 현재 콤보 수
        """
        self._current_combo = combo_count

        if combo_count > self._max_combo:
            self._max_combo = combo_count

        if combo_count > 0:
            self._combo_history.append(combo_count)

    def update_game_duration(self, duration: float) -> None:
        """
        게임 진행 시간 업데이트

        Args:
            duration: 현재까지 진행 시간 (초)
        """
        self._game_duration = duration

    # ============================================================
    # Public Methods - 통계 조회
    # ============================================================

    def get_summary(self) -> Dict:
        """
        통계 요약 반환

        Returns:
            전체 통계 딕셔너리
        """
        total_actions = self._total_jumps + self._total_ducks
        total_perfect = self._perfect_jumps + self._perfect_ducks
        total_obstacles = self._obstacles_avoided + self._obstacles_hit

        return {
            # 행동 통계
            'total_jumps': self._total_jumps,
            'total_ducks': self._total_ducks,
            'perfect_jumps': self._perfect_jumps,
            'perfect_ducks': self._perfect_ducks,
            'total_actions': total_actions,
            'total_perfect_actions': total_perfect,

            # 장애물 통계
            'obstacles_avoided': self._obstacles_avoided,
            'obstacles_hit': self._obstacles_hit,
            'total_obstacles': total_obstacles,
            'success_rate': self._calculate_success_rate(),

            # 콤보 통계
            'current_combo': self._current_combo,
            'max_combo': self._max_combo,
            'avg_combo': self._calculate_average_combo(),

            # 정확도
            'timing_accuracy': self._calculate_timing_accuracy(),
            'perfect_rate': self._calculate_perfect_rate(),

            # 시간
            'game_duration': self._game_duration,
            'actions_per_second': self._calculate_actions_per_second()
        }

    def get_detailed_stats(self) -> Dict:
        """
        상세 통계 반환 (결과 화면용)

        Returns:
            상세 통계 딕셔너리
        """
        summary = self.get_summary()

        return {
            **summary,
            'combo_history': self._combo_history.copy(),
            'timing_accuracy_history': list(self._timing_accuracy_buffer),
            'jump_accuracy': self._calculate_jump_accuracy(),
            'duck_accuracy': self._calculate_duck_accuracy()
        }

    # ============================================================
    # Private Methods - 콤보 관리
    # ============================================================

    def _increment_combo(self) -> None:
        """콤보 증가 (private)"""
        self._current_combo += 1

        if self._current_combo > self._max_combo:
            self._max_combo = self._current_combo

    def _reset_combo(self) -> None:
        """콤보 리셋 (private)"""
        if self._current_combo > 0:
            self._combo_history.append(self._current_combo)

        self._current_combo = 0

    # ============================================================
    # Private Methods - 계산
    # ============================================================

    def _calculate_success_rate(self) -> float:
        """
        장애물 회피 성공률 계산 (private)

        Returns:
            성공률 (0.0~100.0)
        """
        total = self._obstacles_avoided + self._obstacles_hit

        if total == 0:
            return 0.0

        return (self._obstacles_avoided / total) * 100.0

    def _calculate_perfect_rate(self) -> float:
        """
        완벽한 행동 비율 계산 (private)

        Returns:
            완벽한 행동 비율 (0.0~100.0)
        """
        total_actions = self._total_jumps + self._total_ducks

        if total_actions == 0:
            return 0.0

        total_perfect = self._perfect_jumps + self._perfect_ducks
        return (total_perfect / total_actions) * 100.0

    def _calculate_timing_accuracy(self) -> float:
        """
        평균 타이밍 정확도 계산 (private)

        Returns:
            평균 정확도 (0.0~1.0)
        """
        if len(self._timing_accuracy_buffer) == 0:
            return 0.0

        return sum(self._timing_accuracy_buffer) / len(self._timing_accuracy_buffer)

    def _calculate_average_combo(self) -> float:
        """
        평균 콤보 계산 (private)

        Returns:
            평균 콤보 수
        """
        if len(self._combo_history) == 0:
            return 0.0

        return sum(self._combo_history) / len(self._combo_history)

    def _calculate_actions_per_second(self) -> float:
        """
        초당 행동 수 계산 (private)

        Returns:
            초당 행동 수
        """
        if self._game_duration == 0.0:
            return 0.0

        total_actions = self._total_jumps + self._total_ducks
        return total_actions / self._game_duration

    def _calculate_jump_accuracy(self) -> float:
        """점프 정확도 계산 (private)"""
        if self._total_jumps == 0:
            return 0.0

        return (self._perfect_jumps / self._total_jumps) * 100.0

    def _calculate_duck_accuracy(self) -> float:
        """숙이기 정확도 계산 (private)"""
        if self._total_ducks == 0:
            return 0.0

        return (self._perfect_ducks / self._total_ducks) * 100.0

    # ============================================================
    # Getters
    # ============================================================

    @property
    def current_combo(self) -> int:
        """현재 콤보 (읽기 전용)"""
        return self._current_combo

    @property
    def max_combo(self) -> int:
        """최대 콤보 (읽기 전용)"""
        return self._max_combo

    @property
    def obstacles_avoided(self) -> int:
        """회피한 장애물 수 (읽기 전용)"""
        return self._obstacles_avoided

    @property
    def obstacles_hit(self) -> int:
        """충돌한 장애물 수 (읽기 전용)"""
        return self._obstacles_hit

    def reset(self) -> None:
        """통계 초기화"""
        self.__init__()
