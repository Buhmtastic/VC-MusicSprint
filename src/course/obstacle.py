"""
Obstacle 클래스 계층 구조
상속과 다형성을 활용한 장애물 시스템
"""

from abc import ABC, abstractmethod
from typing import Dict, Tuple
from enum import Enum


class ObstacleType(Enum):
    """장애물 타입 열거형"""
    BEAT = "beat"           # 비트 기반 장애물
    FREQUENCY = "frequency" # 주파수 기반 장애물
    AMPLITUDE = "amplitude" # 볼륨 기반 장애물


class Obstacle(ABC):
    """
    추상 장애물 클래스 (Abstract Base Class)

    모든 장애물이 구현해야 하는 공통 인터페이스 정의
    OOP 원칙: 추상화, 다형성
    """

    def __init__(self, time: float, x_position: float):
        """
        장애물 초기화

        Args:
            time: 장애물이 등장하는 시간 (초)
            x_position: X축 위치 (게임 내 좌표)
        """
        self._time = time
        self._x_position = x_position
        self._is_active = True

    @abstractmethod
    def get_height(self) -> float:
        """
        장애물의 높이 반환 (추상 메서드)
        하위 클래스에서 반드시 구현해야 함

        Returns:
            장애물 높이 (픽셀 또는 정규화된 값)
        """
        pass

    @abstractmethod
    def get_width(self) -> float:
        """
        장애물의 너비 반환 (추상 메서드)

        Returns:
            장애물 너비
        """
        pass

    @abstractmethod
    def get_type(self) -> ObstacleType:
        """
        장애물 타입 반환 (추상 메서드)

        Returns:
            ObstacleType 열거형
        """
        pass

    @abstractmethod
    def get_color(self) -> Tuple[int, int, int]:
        """
        장애물 색상 반환 (추상 메서드)

        Returns:
            RGB 튜플 (0-255)
        """
        pass

    def get_info(self) -> Dict:
        """
        장애물 정보 반환

        Returns:
            장애물 정보 딕셔너리
        """
        return {
            'type': self.get_type().value,
            'time': self._time,
            'x_position': self._x_position,
            'height': self.get_height(),
            'width': self.get_width(),
            'color': self.get_color(),
            'is_active': self._is_active
        }

    def deactivate(self) -> None:
        """장애물 비활성화 (통과 후)"""
        self._is_active = False

    @property
    def time(self) -> float:
        """장애물 등장 시간 (읽기 전용)"""
        return self._time

    @property
    def x_position(self) -> float:
        """X축 위치 (읽기 전용)"""
        return self._x_position

    @property
    def is_active(self) -> bool:
        """활성화 상태"""
        return self._is_active


class BeatObstacle(Obstacle):
    """
    비트 기반 장애물
    음악의 비트에 맞춰 등장하는 기본 장애물
    """

    # 클래스 상수
    DEFAULT_HEIGHT = 50.0
    DEFAULT_WIDTH = 20.0
    COLOR = (255, 100, 100)  # 빨간색 계열

    def __init__(self, time: float, x_position: float, beat_strength: float = 1.0):
        """
        비트 장애물 초기화

        Args:
            time: 등장 시간
            x_position: X축 위치
            beat_strength: 비트 강도 (0.0 ~ 1.0), 높이에 영향
        """
        super().__init__(time, x_position)
        self._beat_strength = max(0.0, min(1.0, beat_strength))  # 0~1 클램핑

    def get_height(self) -> float:
        """비트 강도에 따라 높이 조절"""
        return self.DEFAULT_HEIGHT * (0.5 + self._beat_strength * 0.5)

    def get_width(self) -> float:
        """고정 너비 반환"""
        return self.DEFAULT_WIDTH

    def get_type(self) -> ObstacleType:
        """타입 반환"""
        return ObstacleType.BEAT

    def get_color(self) -> Tuple[int, int, int]:
        """색상 반환 (비트 강도에 따라 밝기 조절)"""
        intensity = int(100 + self._beat_strength * 155)
        return (255, intensity, intensity)

    @property
    def beat_strength(self) -> float:
        """비트 강도 (읽기 전용)"""
        return self._beat_strength


class FrequencyWall(Obstacle):
    """
    주파수 기반 장애물
    음악의 주파수 특성에 따라 높이가 변하는 벽
    """

    # 클래스 상수
    MIN_HEIGHT = 30.0
    MAX_HEIGHT = 150.0
    DEFAULT_WIDTH = 15.0
    COLOR = (100, 100, 255)  # 파란색 계열

    def __init__(self, time: float, x_position: float, frequency: float, max_frequency: float = 5000.0):
        """
        주파수 벽 초기화

        Args:
            time: 등장 시간
            x_position: X축 위치
            frequency: 주파수 값 (Hz)
            max_frequency: 최대 주파수 (정규화용)
        """
        super().__init__(time, x_position)
        self._frequency = frequency
        self._max_frequency = max_frequency

        # 주파수를 0~1로 정규화
        self._normalized_frequency = min(frequency / max_frequency, 1.0)

    def get_height(self) -> float:
        """주파수에 비례하는 높이 (고음 = 높은 벽)"""
        return self.MIN_HEIGHT + (self.MAX_HEIGHT - self.MIN_HEIGHT) * self._normalized_frequency

    def get_width(self) -> float:
        """고정 너비"""
        return self.DEFAULT_WIDTH

    def get_type(self) -> ObstacleType:
        """타입 반환"""
        return ObstacleType.FREQUENCY

    def get_color(self) -> Tuple[int, int, int]:
        """주파수에 따라 색상 변화 (저음 = 어두운 파랑, 고음 = 밝은 파랑)"""
        intensity = int(50 + self._normalized_frequency * 205)
        return (intensity // 2, intensity // 2, 255)

    @property
    def frequency(self) -> float:
        """주파수 값 (읽기 전용)"""
        return self._frequency


class AmplitudeGap(Obstacle):
    """
    볼륨 기반 장애물
    음악의 볼륨 변화에 따라 간격이 달라지는 장애물
    """

    # 클래스 상수
    MIN_GAP_HEIGHT = 40.0   # 최소 간격 (통과 공간)
    MAX_GAP_HEIGHT = 120.0  # 최대 간격
    DEFAULT_WIDTH = 25.0
    COLOR = (100, 255, 100)  # 초록색 계열

    def __init__(self, time: float, x_position: float, amplitude: float):
        """
        볼륨 간격 장애물 초기화

        Args:
            time: 등장 시간
            x_position: X축 위치
            amplitude: 진폭(볼륨) 값 (0.0 ~ 1.0 정규화됨)
        """
        super().__init__(time, x_position)
        self._amplitude = max(0.0, min(1.0, amplitude))

    def get_height(self) -> float:
        """
        볼륨에 따라 간격 크기 조절
        볼륨이 클수록 간격이 넓어짐 (쉬움)
        """
        return self.MIN_GAP_HEIGHT + (self.MAX_GAP_HEIGHT - self.MIN_GAP_HEIGHT) * self._amplitude

    def get_width(self) -> float:
        """고정 너비"""
        return self.DEFAULT_WIDTH

    def get_type(self) -> ObstacleType:
        """타입 반환"""
        return ObstacleType.AMPLITUDE

    def get_color(self) -> Tuple[int, int, int]:
        """볼륨에 따라 색상 밝기 조절"""
        intensity = int(100 + self._amplitude * 155)
        return (intensity, 255, intensity)

    @property
    def amplitude(self) -> float:
        """진폭 값 (읽기 전용)"""
        return self._amplitude


# 다형성 테스트용 헬퍼 함수
def print_obstacle_info(obstacle: Obstacle) -> None:
    """
    다형성 데모: 모든 Obstacle 타입을 동일하게 처리

    Args:
        obstacle: 임의의 Obstacle 하위 클래스 인스턴스
    """
    info = obstacle.get_info()
    print(f"[{info['type'].upper()}] "
          f"Time: {info['time']:.2f}s, "
          f"Height: {info['height']:.1f}, "
          f"Color: {info['color']}")
