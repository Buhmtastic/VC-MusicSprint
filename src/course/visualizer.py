"""
Course Visualizer
생성된 코스를 시각화하여 정적 이미지로 출력
"""

from typing import Optional
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path
from .course import Course
from .obstacle import ObstacleType


class CourseVisualizer:
    """
    코스 시각화 클래스

    책임:
    - 생성된 코스를 matplotlib로 시각화
    - 장애물 타입별 색상 구분
    - 정적 이미지 파일로 저장
    """

    # 시각화 설정
    FIGURE_WIDTH = 16
    FIGURE_HEIGHT = 6
    DPI = 100

    # 축 설정
    Y_AXIS_HEIGHT = 200  # Y축 높이 (픽셀 단위)

    def __init__(self):
        """Visualizer 초기화"""
        pass

    def visualize(
        self,
        course: Course,
        output_path: Optional[str] = None,
        show: bool = True
    ) -> None:
        """
        코스를 시각화하여 표시/저장

        Args:
            course: 시각화할 Course 객체
            output_path: 저장할 파일 경로 (None이면 저장 안 함)
            show: plt.show() 호출 여부
        """
        if not course.is_finalized:
            raise ValueError("코스가 finalize되지 않았습니다.")

        # Figure 생성
        fig, ax = plt.subplots(figsize=(self.FIGURE_WIDTH, self.FIGURE_HEIGHT))

        # 배경 설정
        ax.set_facecolor('#1a1a2e')
        fig.patch.set_facecolor('#0f0f1e')

        # 축 설정
        ax.set_xlim(0, course.duration)
        ax.set_ylim(0, self.Y_AXIS_HEIGHT)
        ax.set_xlabel('Time (seconds)', color='white', fontsize=12)
        ax.set_ylabel('Obstacle Height', color='white', fontsize=12)
        ax.set_title(f'Course: {course.name} ({course.obstacle_count} obstacles)',
                     color='white', fontsize=14, fontweight='bold')

        # 그리드
        ax.grid(True, alpha=0.2, color='white', linestyle='--', linewidth=0.5)

        # 축 색상
        ax.tick_params(colors='white')
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # 장애물 그리기
        for obstacle in course.obstacles:
            self._draw_obstacle(ax, obstacle)

        # 범례 추가
        self._add_legend(ax)

        # 통계 정보 추가
        self._add_statistics(ax, course)

        # 레이아웃 조정
        plt.tight_layout()

        # 저장
        if output_path:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(output_path, dpi=self.DPI, facecolor=fig.get_facecolor())
            print(f"✅ 코스 시각화 저장: {output_path}")

        # 표시
        if show:
            plt.show()
        else:
            plt.close()

    def _draw_obstacle(self, ax, obstacle) -> None:
        """
        개별 장애물을 그리기 (private 메서드)

        Args:
            ax: matplotlib Axes 객체
            obstacle: 그릴 Obstacle 객체
        """
        time = obstacle.time
        height = obstacle.get_height()
        width = 0.05  # 시각화용 너비 (시간 단위)

        # 색상 (RGB → 정규화)
        color_rgb = obstacle.get_color()
        color_normalized = tuple(c / 255.0 for c in color_rgb)

        # 사각형 그리기
        rect = patches.Rectangle(
            (time - width/2, 0),  # (x, y) 시작점
            width,                # 너비
            height,               # 높이
            linewidth=1,
            edgecolor='white',
            facecolor=color_normalized,
            alpha=0.8
        )
        ax.add_patch(rect)

        # 타입별 마커 추가
        obstacle_type = obstacle.get_type()
        if obstacle_type == ObstacleType.BEAT:
            marker = 'o'
        elif obstacle_type == ObstacleType.FREQUENCY:
            marker = 's'
        else:  # AMPLITUDE
            marker = '^'

        ax.plot(time, height, marker=marker, color=color_normalized,
                markersize=4, markeredgecolor='white', markeredgewidth=0.5)

    def _add_legend(self, ax) -> None:
        """
        범례 추가 (private 메서드)

        Args:
            ax: matplotlib Axes 객체
        """
        from matplotlib.lines import Line2D

        legend_elements = [
            Line2D([0], [0], marker='o', color='w', markerfacecolor='#ff6464',
                   markersize=8, label='Beat Obstacle', linestyle='None'),
            Line2D([0], [0], marker='s', color='w', markerfacecolor='#6464ff',
                   markersize=8, label='Frequency Wall', linestyle='None'),
            Line2D([0], [0], marker='^', color='w', markerfacecolor='#64ff64',
                   markersize=8, label='Amplitude Gap', linestyle='None')
        ]

        ax.legend(handles=legend_elements, loc='upper right',
                  facecolor='#2a2a3e', edgecolor='white',
                  labelcolor='white', fontsize=10)

    def _add_statistics(self, ax, course: Course) -> None:
        """
        통계 정보를 이미지에 추가 (private 메서드)

        Args:
            ax: matplotlib Axes 객체
            course: Course 객체
        """
        stats = course.get_statistics()

        # 통계 텍스트 생성
        stats_text = (
            f"Duration: {stats['duration']:.1f}s\n"
            f"Total: {stats['total_obstacles']} obstacles\n"
            f"Density: {stats['density']:.2f} obs/s\n"
            f"Beat: {stats['by_type']['beat']}\n"
            f"Freq: {stats['by_type']['frequency']}\n"
            f"Amp: {stats['by_type']['amplitude']}"
        )

        # 텍스트 박스 추가
        ax.text(
            0.02, 0.98, stats_text,
            transform=ax.transAxes,
            fontsize=10,
            verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='#2a2a3e', alpha=0.8, edgecolor='white'),
            color='white',
            family='monospace'
        )

    def compare_courses(
        self,
        courses: list,
        output_path: Optional[str] = None,
        show: bool = True
    ) -> None:
        """
        여러 코스를 나란히 비교 시각화

        Args:
            courses: Course 객체 리스트 (최대 3개 권장)
            output_path: 저장 경로
            show: 표시 여부
        """
        num_courses = len(courses)
        if num_courses == 0:
            raise ValueError("비교할 코스가 없습니다.")

        # 서브플롯 생성
        fig, axes = plt.subplots(num_courses, 1,
                                 figsize=(self.FIGURE_WIDTH, self.FIGURE_HEIGHT * num_courses / 2))

        if num_courses == 1:
            axes = [axes]  # 단일 코스도 리스트로 처리

        fig.patch.set_facecolor('#0f0f1e')
        fig.suptitle('Course Comparison', color='white', fontsize=16, fontweight='bold')

        for i, (course, ax) in enumerate(zip(courses, axes)):
            if not course.is_finalized:
                raise ValueError(f"코스 {i+1}이 finalize되지 않았습니다.")

            # 각 코스 시각화
            ax.set_facecolor('#1a1a2e')
            ax.set_xlim(0, course.duration)
            ax.set_ylim(0, self.Y_AXIS_HEIGHT)
            ax.set_xlabel('Time (s)', color='white')
            ax.set_ylabel('Height', color='white')
            ax.set_title(course.name, color='white', fontsize=12)
            ax.grid(True, alpha=0.2, color='white')
            ax.tick_params(colors='white')

            for obstacle in course.obstacles:
                self._draw_obstacle(ax, obstacle)

        plt.tight_layout()

        if output_path:
            plt.savefig(output_path, dpi=self.DPI, facecolor=fig.get_facecolor())
            print(f"✅ 코스 비교 시각화 저장: {output_path}")

        if show:
            plt.show()
        else:
            plt.close()
