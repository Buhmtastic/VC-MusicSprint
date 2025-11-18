# -*- coding: utf-8 -*-
"""
Game Renderer
PyGame을 사용한 게임 렌더링

책임:
- 캐릭터 애니메이션 렌더링
- 장애물 렌더링
- 파형 배경 렌더링
- UI 요소 (점수, 시간) 표시
"""

import pygame
import numpy as np
from typing import Optional, List
from .game import Game
from .character import CharacterState
from ..course.obstacle import Obstacle, ObstacleType


class GameRenderer:
    """
    게임 렌더러 클래스

    OOP 원칙:
    - 단일 책임: 렌더링만 담당
    - 의존성 분리: Game 객체에 의존하지만 수정하지 않음
    """

    # 화면 설정
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    FPS = 60

    # 색상 (RGB)
    COLOR_BACKGROUND = (20, 20, 30)
    COLOR_GROUND = (60, 60, 80)
    COLOR_CHARACTER = (255, 200, 100)
    COLOR_CHARACTER_OUTLINE = (255, 255, 255)
    COLOR_TEXT = (255, 255, 255)
    COLOR_WAVEFORM = (100, 150, 255)

    # 캐릭터 애니메이션
    ANIMATION_FRAME_DURATION = 0.15  # 프레임당 지속 시간 (초)

    def __init__(self, game: Game):
        """
        렌더러 초기화

        Args:
            game: 렌더링할 Game 객체
        """
        self._game = game

        # PyGame 초기화
        pygame.init()
        self._screen = pygame.display.set_mode(
            (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        )
        pygame.display.set_caption("Music Sprint - Phase 3")

        # 폰트 초기화
        self._font_large = pygame.font.Font(None, 48)
        self._font_medium = pygame.font.Font(None, 32)
        self._font_small = pygame.font.Font(None, 24)

        # 애니메이션 타이머
        self._animation_time = 0.0
        self._current_frame = 0

        # 클록
        self._clock = pygame.time.Clock()

    # ============================================================
    # Public Methods - 렌더링
    # ============================================================

    def render(self, delta_time: float) -> None:
        """
        화면 렌더링

        Args:
            delta_time: 이전 프레임으로부터 경과 시간
        """
        # 배경 그리기
        self._draw_background()

        # 파형 렌더링
        self._draw_waveform()

        # 지면 그리기
        self._draw_ground()

        # 장애물 그리기
        self._draw_obstacles()

        # 캐릭터 그리기
        self._draw_character(delta_time)

        # UI 그리기
        self._draw_ui()

        # 화면 업데이트
        pygame.display.flip()
        self._clock.tick(self.FPS)

    def render_start_screen(self) -> None:
        """시작 화면 렌더링"""
        self._screen.fill(self.COLOR_BACKGROUND)

        # 타이틀
        title = self._font_large.render("Music Sprint", True, self.COLOR_TEXT)
        title_rect = title.get_rect(center=(self.SCREEN_WIDTH // 2, 200))
        self._screen.blit(title, title_rect)

        # 안내 문구
        subtitle = self._font_medium.render(
            "Auto-Play Demo", True, self.COLOR_TEXT
        )
        subtitle_rect = subtitle.get_rect(center=(self.SCREEN_WIDTH // 2, 300))
        self._screen.blit(subtitle, subtitle_rect)

        instruction = self._font_small.render(
            "Press SPACE to start", True, self.COLOR_TEXT
        )
        instruction_rect = instruction.get_rect(center=(self.SCREEN_WIDTH // 2, 400))
        self._screen.blit(instruction, instruction_rect)

        pygame.display.flip()

    def render_end_screen(self) -> None:
        """종료 화면 렌더링"""
        self._screen.fill(self.COLOR_BACKGROUND)

        stats = self._game.get_statistics()

        # 결과
        title = self._font_large.render("Game Finished!", True, self.COLOR_TEXT)
        title_rect = title.get_rect(center=(self.SCREEN_WIDTH // 2, 150))
        self._screen.blit(title, title_rect)

        # 통계
        y_offset = 250
        stats_lines = [
            f"Score: {stats['score']}",
            f"Success Rate: {stats['success_rate']:.1f}%",
            f"Avoided: {stats['obstacles_avoided']}",
            f"Hit: {stats['obstacles_hit']}",
            f"Perfect: {stats['perfect_dodges']}"
        ]

        for line in stats_lines:
            text = self._font_medium.render(line, True, self.COLOR_TEXT)
            text_rect = text.get_rect(center=(self.SCREEN_WIDTH // 2, y_offset))
            self._screen.blit(text, text_rect)
            y_offset += 40

        # 안내
        instruction = self._font_small.render(
            "Press ESC to exit", True, self.COLOR_TEXT
        )
        instruction_rect = instruction.get_rect(center=(self.SCREEN_WIDTH // 2, 500))
        self._screen.blit(instruction, instruction_rect)

        pygame.display.flip()

    def get_delta_time(self) -> float:
        """
        델타 타임 계산 (초)

        Returns:
            이전 프레임으로부터 경과 시간
        """
        return self._clock.get_time() / 1000.0

    # ============================================================
    # Private Methods - 렌더링 세부사항
    # ============================================================

    def _draw_background(self) -> None:
        """배경 그리기"""
        self._screen.fill(self.COLOR_BACKGROUND)

    def _draw_ground(self) -> None:
        """지면 그리기"""
        ground_y = int(self._game.character.GROUND_Y)
        pygame.draw.line(
            self._screen,
            self.COLOR_GROUND,
            (0, ground_y),
            (self.SCREEN_WIDTH, ground_y),
            3
        )

    def _draw_waveform(self) -> None:
        """파형 배경 렌더링"""
        waveform = self._game.get_waveform_slice(window_duration=2.0)

        if waveform is None or len(waveform) == 0:
            return

        # 파형 다운샘플링 (화면 너비에 맞춤)
        num_points = min(len(waveform), self.SCREEN_WIDTH)
        step = len(waveform) // num_points if num_points > 0 else 1

        points = []
        for i in range(num_points):
            idx = i * step
            if idx >= len(waveform):
                break

            # 파형 값을 화면 좌표로 변환
            x = i
            amplitude = waveform[idx]
            y = int(self.SCREEN_HEIGHT / 2 + amplitude * 100)

            # 범위 제한
            y = max(0, min(self.SCREEN_HEIGHT, y))
            points.append((x, y))

        # 파형 그리기
        if len(points) > 1:
            pygame.draw.lines(
                self._screen,
                self.COLOR_WAVEFORM,
                False,
                points,
                2
            )

    def _draw_obstacles(self) -> None:
        """장애물 렌더링"""
        active_obstacles = self._game.active_obstacles
        current_time = self._game.current_time
        char_x = self._game.character.x

        for obstacle in active_obstacles:
            # 장애물의 화면상 위치 계산
            time_diff = obstacle.time - current_time
            obstacle_x = char_x + time_diff * self._game.GAME_SPEED

            # 화면 밖이면 렌더링 안 함
            if obstacle_x < -50 or obstacle_x > self.SCREEN_WIDTH + 50:
                continue

            # 장애물 그리기
            self._draw_single_obstacle(obstacle, obstacle_x)

    def _draw_single_obstacle(self, obstacle: Obstacle, x: float) -> None:
        """
        개별 장애물 렌더링

        Args:
            obstacle: 장애물 객체
            x: 화면상 X 좌표
        """
        height = obstacle.get_height()
        color = obstacle.get_color()
        obs_type = obstacle.get_type()

        # Y 위치 (지면에서 위로)
        y = int(self._game.character.GROUND_Y - height)
        width = 20

        # 색상 정규화
        color_normalized = tuple(int(c) for c in color)

        # 사각형 그리기
        rect = pygame.Rect(int(x) - width // 2, y, width, int(height))
        pygame.draw.rect(self._screen, color_normalized, rect)
        pygame.draw.rect(self._screen, self.COLOR_CHARACTER_OUTLINE, rect, 2)

        # 타입별 마커 (선택)
        if obs_type == ObstacleType.BEAT:
            # 원형 마커
            pygame.draw.circle(
                self._screen,
                color_normalized,
                (int(x), y + int(height) // 2),
                5
            )

    def _draw_character(self, delta_time: float) -> None:
        """
        캐릭터 애니메이션 렌더링

        Args:
            delta_time: 델타 타임
        """
        character = self._game.character
        char_x = int(character.x)
        char_y = int(character.y)
        char_w = int(character.width)
        char_h = int(character.height)

        # 애니메이션 프레임 업데이트
        self._animation_time += delta_time
        if self._animation_time >= self.ANIMATION_FRAME_DURATION:
            self._animation_time = 0.0
            self._current_frame = (self._current_frame + 1) % 3

        # 상태별 색상 변경
        if character.state == CharacterState.JUMPING:
            color = (100, 255, 100)  # 녹색
        elif character.state == CharacterState.DUCKING:
            color = (255, 100, 100)  # 빨간색
        else:
            color = self.COLOR_CHARACTER  # 주황색

        # 캐릭터 사각형
        char_rect = pygame.Rect(char_x, char_y, char_w, char_h)
        pygame.draw.rect(self._screen, color, char_rect)
        pygame.draw.rect(self._screen, self.COLOR_CHARACTER_OUTLINE, char_rect, 2)

        # 간단한 애니메이션 (점 3개로 달리는 표현)
        if character.state == CharacterState.RUNNING:
            frame_offset = self._current_frame * 5
            pygame.draw.circle(
                self._screen,
                self.COLOR_CHARACTER_OUTLINE,
                (char_x + char_w // 2, char_y + char_h - 5 - frame_offset),
                3
            )

    def _draw_ui(self) -> None:
        """UI 요소 렌더링"""
        stats = self._game.get_statistics()

        # 점수
        score_text = self._font_medium.render(
            f"Score: {stats['score']}", True, self.COLOR_TEXT
        )
        self._screen.blit(score_text, (10, 10))

        # 시간
        time_text = self._font_small.render(
            f"Time: {stats['current_time']:.1f}s / {stats['duration']:.1f}s",
            True, self.COLOR_TEXT
        )
        self._screen.blit(time_text, (10, 50))

        # 진행률
        progress_text = self._font_small.render(
            f"Progress: {stats['progress']:.1f}%", True, self.COLOR_TEXT
        )
        self._screen.blit(progress_text, (10, 80))

        # 통계
        stats_text = self._font_small.render(
            f"Avoided: {stats['obstacles_avoided']} | Hit: {stats['obstacles_hit']}",
            True, self.COLOR_TEXT
        )
        self._screen.blit(stats_text, (10, 110))

    def cleanup(self) -> None:
        """리소스 정리"""
        pygame.quit()
