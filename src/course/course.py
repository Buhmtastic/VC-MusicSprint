"""
Course 클래스
게임 코스 및 장애물 타임라인 관리
"""

from typing import List, Dict, Optional
from .obstacle import Obstacle, ObstacleType


class Course:
    """
    게임 코스 클래스

    책임:
    - 장애물 리스트 관리
    - 시간 기반 장애물 타임라인 관리
    - 특정 시간의 장애물 조회

    OOP 원칙: 캡슐화 - 내부 데이터 직접 접근 불가
    """

    def __init__(self, duration: float, name: str = "Unnamed Course"):
        """
        코스 초기화

        Args:
            duration: 코스 총 길이 (초)
            name: 코스 이름
        """
        self._duration = duration
        self._name = name
        self._obstacles: List[Obstacle] = []  # Private: 장애물 리스트
        self._timeline: Dict[float, List[Obstacle]] = {}  # Private: 시간별 장애물 매핑
        self._is_finalized = False

    def add_obstacle(self, obstacle: Obstacle) -> None:
        """
        코스에 장애물 추가

        Args:
            obstacle: 추가할 장애물 객체

        Raises:
            ValueError: 코스가 이미 finalize된 경우
        """
        if self._is_finalized:
            raise ValueError("코스가 이미 finalize되었습니다. 장애물을 추가할 수 없습니다.")

        # 장애물 시간이 코스 범위 내인지 확인
        if obstacle.time < 0 or obstacle.time > self._duration:
            raise ValueError(
                f"장애물 시간({obstacle.time:.2f}s)이 코스 범위(0~{self._duration:.2f}s)를 벗어났습니다."
            )

        self._obstacles.append(obstacle)

    def add_obstacles(self, obstacles: List[Obstacle]) -> None:
        """
        여러 장애물을 한 번에 추가

        Args:
            obstacles: 장애물 리스트
        """
        for obstacle in obstacles:
            self.add_obstacle(obstacle)

    def finalize(self) -> None:
        """
        코스 최종화

        - 장애물을 시간 순으로 정렬
        - 타임라인 딕셔너리 생성
        - 이후 장애물 추가 불가
        """
        # 시간 순으로 정렬
        self._obstacles.sort(key=lambda obs: obs.time)

        # 타임라인 생성 (시간을 0.1초 단위로 반올림하여 그룹화)
        self._timeline = {}
        for obstacle in self._obstacles:
            # 0.1초 단위로 반올림
            time_key = round(obstacle.time, 1)

            if time_key not in self._timeline:
                self._timeline[time_key] = []

            self._timeline[time_key].append(obstacle)

        self._is_finalized = True

    def get_obstacles_at_time(self, time: float, tolerance: float = 0.1) -> List[Obstacle]:
        """
        특정 시간에 존재하는 장애물 조회

        Args:
            time: 조회할 시간 (초)
            tolerance: 시간 허용 오차 (초)

        Returns:
            해당 시간의 장애물 리스트
        """
        if not self._is_finalized:
            raise RuntimeError("코스가 finalize되지 않았습니다. finalize()를 먼저 호출하세요.")

        # 타임라인에서 정확한 키 조회
        time_key = round(time, 1)

        if time_key in self._timeline:
            return self._timeline[time_key].copy()

        # 허용 오차 범위 내에서 검색
        nearby_obstacles = []
        for obstacle in self._obstacles:
            if abs(obstacle.time - time) <= tolerance:
                nearby_obstacles.append(obstacle)

        return nearby_obstacles

    def get_obstacles_in_range(self, start_time: float, end_time: float) -> List[Obstacle]:
        """
        시간 범위 내의 모든 장애물 조회

        Args:
            start_time: 시작 시간
            end_time: 종료 시간

        Returns:
            해당 범위의 장애물 리스트
        """
        if not self._is_finalized:
            raise RuntimeError("코스가 finalize되지 않았습니다.")

        return [
            obs for obs in self._obstacles
            if start_time <= obs.time <= end_time
        ]

    def get_obstacle_count_by_type(self) -> Dict[str, int]:
        """
        타입별 장애물 개수 집계

        Returns:
            타입별 개수 딕셔너리
        """
        counts = {
            ObstacleType.BEAT.value: 0,
            ObstacleType.FREQUENCY.value: 0,
            ObstacleType.AMPLITUDE.value: 0
        }

        for obstacle in self._obstacles:
            counts[obstacle.get_type().value] += 1

        return counts

    def get_statistics(self) -> Dict:
        """
        코스 통계 정보 반환

        Returns:
            통계 딕셔너리
        """
        if not self._obstacles:
            return {
                'name': self._name,
                'duration': self._duration,
                'total_obstacles': 0,
                'by_type': {},
                'density': 0.0
            }

        return {
            'name': self._name,
            'duration': self._duration,
            'total_obstacles': len(self._obstacles),
            'by_type': self.get_obstacle_count_by_type(),
            'density': len(self._obstacles) / self._duration if self._duration > 0 else 0,
            'first_obstacle_time': self._obstacles[0].time if self._obstacles else None,
            'last_obstacle_time': self._obstacles[-1].time if self._obstacles else None,
            'is_finalized': self._is_finalized
        }

    def clear(self) -> None:
        """코스 초기화 (모든 장애물 제거)"""
        self._obstacles.clear()
        self._timeline.clear()
        self._is_finalized = False

    @property
    def duration(self) -> float:
        """코스 길이 (읽기 전용)"""
        return self._duration

    @property
    def name(self) -> str:
        """코스 이름 (읽기 전용)"""
        return self._name

    @property
    def obstacle_count(self) -> int:
        """전체 장애물 개수 (읽기 전용)"""
        return len(self._obstacles)

    @property
    def obstacles(self) -> List[Obstacle]:
        """
        장애물 리스트 (읽기 전용, 복사본 반환)
        원본 보호를 위해 복사본 반환
        """
        return self._obstacles.copy()

    @property
    def is_finalized(self) -> bool:
        """최종화 여부 (읽기 전용)"""
        return self._is_finalized

    def __repr__(self) -> str:
        """문자열 표현"""
        return (f"Course(name='{self._name}', duration={self._duration:.1f}s, "
                f"obstacles={len(self._obstacles)}, finalized={self._is_finalized})")

    def __len__(self) -> int:
        """len(course) 지원"""
        return len(self._obstacles)
