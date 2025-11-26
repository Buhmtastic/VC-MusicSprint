# -*- coding: utf-8 -*-
"""
Result Screen
게임 결과 화면 및 통계 시각화

책임:
- 게임 종료 후 결과 표시
- matplotlib을 사용한 통계 그래프
- 하이스코어 비교 및 표시
- 결과 화면 PNG 저장
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from typing import Dict, Optional, List
import os


class ResultScreen:
    """
    결과 화면 클래스

    OOP 원칙:
    - 단일 책임: 결과 시각화만 담당
    - 캡슐화: 내부 그래프 생성 로직 은닉
    """

    # 색상 팔레트
    COLOR_PRIMARY = '#4A90E2'
    COLOR_SUCCESS = '#7ED321'
    COLOR_WARNING = '#F5A623'
    COLOR_DANGER = '#D0021B'
    COLOR_BACKGROUND = '#F8F9FA'
    COLOR_TEXT = '#2C3E50'

    def __init__(self, save_directory: str = 'assets/results'):
        """
        ResultScreen 초기화

        Args:
            save_directory: 결과 이미지 저장 디렉토리
        """
        self._save_directory = save_directory

        # 디렉토리 생성
        os.makedirs(save_directory, exist_ok=True)

    def display_and_save(
        self,
        game_stats: Dict,
        score_info: Dict,
        high_score_data: Optional[Dict] = None,
        filename: str = 'game_result.png'
    ) -> str:
        """
        결과 화면 생성 및 저장

        Args:
            game_stats: 게임 통계 (Game.get_statistics() 반환값)
            score_info: 점수 정보 (ScoreManager.calculate_final_score() 반환값)
            high_score_data: 하이스코어 데이터 (선택)
            filename: 저장할 파일명

        Returns:
            저장된 파일 경로
        """
        # Figure 생성 (3x2 레이아웃)
        fig = plt.figure(figsize=(16, 10))
        fig.suptitle('Music Sprint - Game Results', fontsize=20, fontweight='bold')

        # 1. 점수 요약 (좌측 상단)
        ax1 = plt.subplot(2, 3, 1)
        self._draw_score_summary(ax1, game_stats, score_info)

        # 2. 난이도 정보 (우측 상단)
        ax2 = plt.subplot(2, 3, 2)
        self._draw_difficulty_info(ax2, game_stats, score_info)

        # 3. 하이스코어 비교 (중앙 상단)
        ax3 = plt.subplot(2, 3, 3)
        self._draw_high_score_comparison(ax3, score_info, high_score_data)

        # 4. 성공률 및 콤보 (좌측 하단)
        ax4 = plt.subplot(2, 3, 4)
        self._draw_success_rate_chart(ax4, game_stats)

        # 5. 정확도 게이지 (중앙 하단)
        ax5 = plt.subplot(2, 3, 5)
        self._draw_accuracy_gauge(ax5, game_stats)

        # 6. 통계 요약 (우측 하단)
        ax6 = plt.subplot(2, 3, 6)
        self._draw_statistics_table(ax6, game_stats, score_info)

        # 레이아웃 조정
        plt.tight_layout(rect=[0, 0.03, 1, 0.96])

        # 저장
        save_path = os.path.join(self._save_directory, filename)
        plt.savefig(save_path, dpi=150, bbox_inches='tight', facecolor='white')
        print(f"\n[Result Screen] Saved to: {save_path}")

        # 화면에 표시
        plt.show(block=False)
        plt.pause(0.1)

        return save_path

    # ============================================================
    # Private Methods - 개별 차트 렌더링
    # ============================================================

    def _draw_score_summary(self, ax, game_stats: Dict, score_info: Dict) -> None:
        """점수 요약 렌더링"""
        ax.axis('off')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)

        # 최종 점수 (크게)
        final_score = score_info.get('final_score', 0)
        ax.text(
            0.5, 0.7,
            f"{final_score:,}",
            fontsize=48,
            fontweight='bold',
            ha='center',
            va='center',
            color=self.COLOR_PRIMARY
        )

        ax.text(
            0.5, 0.5,
            "FINAL SCORE",
            fontsize=16,
            ha='center',
            va='center',
            color=self.COLOR_TEXT,
            alpha=0.7
        )

        # 기본 점수 및 배율
        base_score = score_info.get('base_score', 0)
        difficulty_multiplier = score_info.get('difficulty_multiplier', 1.0)

        details = f"Base: {base_score:,}\n"
        details += f"Multiplier: {difficulty_multiplier:.1f}x"

        ax.text(
            0.5, 0.25,
            details,
            fontsize=12,
            ha='center',
            va='center',
            color=self.COLOR_TEXT,
            alpha=0.6
        )

        ax.set_title('Score Summary', fontsize=14, fontweight='bold', pad=10)

    def _draw_difficulty_info(self, ax, game_stats: Dict, score_info: Dict) -> None:
        """난이도 정보 렌더링"""
        ax.axis('off')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)

        difficulty_level = game_stats.get('difficulty_level', 'normal').upper()
        difficulty_score = game_stats.get('difficulty_score', 50.0)

        # 난이도 레벨별 색상
        color_map = {
            'EASY': self.COLOR_SUCCESS,
            'NORMAL': self.COLOR_PRIMARY,
            'HARD': self.COLOR_WARNING,
            'EXPERT': self.COLOR_DANGER
        }
        color = color_map.get(difficulty_level, self.COLOR_PRIMARY)

        # 난이도 레벨
        ax.text(
            0.5, 0.7,
            difficulty_level,
            fontsize=36,
            fontweight='bold',
            ha='center',
            va='center',
            color=color
        )

        ax.text(
            0.5, 0.5,
            f"Difficulty Score: {difficulty_score:.1f}/100",
            fontsize=12,
            ha='center',
            va='center',
            color=self.COLOR_TEXT,
            alpha=0.7
        )

        # 난이도 바
        bar_width = 0.6
        bar_height = 0.05
        bar_x = 0.2
        bar_y = 0.3

        # 배경 바
        bg_rect = mpatches.Rectangle(
            (bar_x, bar_y), bar_width, bar_height,
            facecolor='lightgray',
            edgecolor='none',
            transform=ax.transAxes
        )
        ax.add_patch(bg_rect)

        # 진행 바
        progress_width = bar_width * (difficulty_score / 100.0)
        progress_rect = mpatches.Rectangle(
            (bar_x, bar_y), progress_width, bar_height,
            facecolor=color,
            edgecolor='none',
            transform=ax.transAxes
        )
        ax.add_patch(progress_rect)

        ax.set_title('Difficulty', fontsize=14, fontweight='bold', pad=10)

    def _draw_high_score_comparison(
        self,
        ax,
        score_info: Dict,
        high_score_data: Optional[Dict]
    ) -> None:
        """하이스코어 비교 차트"""
        ax.axis('off')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)

        current_score = score_info.get('final_score', 0)

        if high_score_data and 'score' in high_score_data:
            high_score = high_score_data['score']

            # 신기록 여부
            is_new_record = current_score >= high_score

            if is_new_record:
                ax.text(
                    0.5, 0.7,
                    "🏆 NEW RECORD!",
                    fontsize=24,
                    fontweight='bold',
                    ha='center',
                    va='center',
                    color=self.COLOR_WARNING
                )
            else:
                ax.text(
                    0.5, 0.7,
                    "High Score",
                    fontsize=18,
                    ha='center',
                    va='center',
                    color=self.COLOR_TEXT
                )

            # 점수 비교
            comparison = f"Current: {current_score:,}\n"
            comparison += f"Best: {high_score:,}\n"
            diff = current_score - high_score
            comparison += f"Diff: {diff:+,}"

            ax.text(
                0.5, 0.4,
                comparison,
                fontsize=12,
                ha='center',
                va='center',
                color=self.COLOR_TEXT,
                alpha=0.8
            )
        else:
            # 첫 플레이
            ax.text(
                0.5, 0.6,
                "First Play!",
                fontsize=20,
                fontweight='bold',
                ha='center',
                va='center',
                color=self.COLOR_PRIMARY
            )

            ax.text(
                0.5, 0.4,
                f"Score: {current_score:,}",
                fontsize=14,
                ha='center',
                va='center',
                color=self.COLOR_TEXT,
                alpha=0.7
            )

        ax.set_title('High Score', fontsize=14, fontweight='bold', pad=10)

    def _draw_success_rate_chart(self, ax, game_stats: Dict) -> None:
        """성공률 및 콤보 차트"""
        success_rate = game_stats.get('success_rate', 0.0)
        max_combo = game_stats.get('max_combo', 0)
        obstacles_avoided = game_stats.get('obstacles_avoided', 0)
        obstacles_hit = game_stats.get('obstacles_hit', 0)

        # 파이 차트
        sizes = [obstacles_avoided, obstacles_hit]
        colors = [self.COLOR_SUCCESS, self.COLOR_DANGER]
        labels = [f'Avoided\n{obstacles_avoided}', f'Hit\n{obstacles_hit}']

        if sum(sizes) > 0:
            wedges, texts, autotexts = ax.pie(
                sizes,
                labels=labels,
                colors=colors,
                autopct='%1.1f%%',
                startangle=90,
                textprops={'fontsize': 10}
            )
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
        else:
            ax.text(0.5, 0.5, 'No Data', ha='center', va='center')

        # 최대 콤보 표시
        ax.text(
            0.0, -1.3,
            f"Max Combo: {max_combo}",
            fontsize=12,
            ha='center',
            va='center',
            color=self.COLOR_PRIMARY,
            fontweight='bold'
        )

        ax.set_title('Success Rate', fontsize=14, fontweight='bold', pad=10)

    def _draw_accuracy_gauge(self, ax, game_stats: Dict) -> None:
        """정확도 게이지"""
        timing_accuracy = game_stats.get('timing_accuracy', 0.0)

        # 게이지 차트 (반원형)
        theta = (1 - timing_accuracy) * 180  # 0도 = 100%, 180도 = 0%

        # 배경 호
        bg_wedge = mpatches.Wedge(
            (0.5, 0.3), 0.4, 0, 180,
            width=0.1,
            facecolor='lightgray',
            edgecolor='none',
            transform=ax.transAxes
        )
        ax.add_patch(bg_wedge)

        # 정확도 호
        accuracy_color = self.COLOR_SUCCESS if timing_accuracy >= 0.7 else \
                        self.COLOR_WARNING if timing_accuracy >= 0.5 else \
                        self.COLOR_DANGER

        accuracy_wedge = mpatches.Wedge(
            (0.5, 0.3), 0.4, 0, 180 * timing_accuracy,
            width=0.1,
            facecolor=accuracy_color,
            edgecolor='none',
            transform=ax.transAxes
        )
        ax.add_patch(accuracy_wedge)

        # 중앙 텍스트
        ax.text(
            0.5, 0.35,
            f"{timing_accuracy * 100:.1f}%",
            fontsize=28,
            fontweight='bold',
            ha='center',
            va='center',
            color=accuracy_color,
            transform=ax.transAxes
        )

        ax.text(
            0.5, 0.15,
            "Timing Accuracy",
            fontsize=12,
            ha='center',
            va='center',
            color=self.COLOR_TEXT,
            alpha=0.7,
            transform=ax.transAxes
        )

        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        ax.set_title('Accuracy', fontsize=14, fontweight='bold', pad=10)

    def _draw_statistics_table(self, ax, game_stats: Dict, score_info: Dict) -> None:
        """통계 요약 테이블"""
        ax.axis('off')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)

        # 통계 데이터
        stats_data = [
            ['Duration', f"{game_stats.get('duration', 0):.1f}s"],
            ['Obstacles', f"{game_stats.get('obstacles_avoided', 0) + game_stats.get('obstacles_hit', 0)}"],
            ['Perfect Dodges', f"{game_stats.get('perfect_dodges', 0)}"],
            ['Combo Multiplier', f"{score_info.get('combo_multiplier', 1.0):.2f}x"],
            ['Accuracy Bonus', f"{score_info.get('accuracy_multiplier', 1.0):.2f}x"],
        ]

        # 테이블 렌더링
        y_position = 0.85
        for label, value in stats_data:
            # 라벨
            ax.text(
                0.1, y_position,
                label,
                fontsize=11,
                ha='left',
                va='center',
                color=self.COLOR_TEXT,
                alpha=0.7
            )

            # 값
            ax.text(
                0.9, y_position,
                value,
                fontsize=11,
                ha='right',
                va='center',
                color=self.COLOR_TEXT,
                fontweight='bold'
            )

            y_position -= 0.15

        ax.set_title('Statistics', fontsize=14, fontweight='bold', pad=10)

    def close(self) -> None:
        """matplotlib 창 닫기"""
        plt.close('all')
