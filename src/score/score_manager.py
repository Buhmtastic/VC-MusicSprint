# -*- coding: utf-8 -*-
"""
ScoreManager Class
점수 계산 및 하이스코어 관리

책임:
- 점수 계산 (거리, 정확도, 콤보 기반)
- 난이도 배율 적용
- 하이스코어 저장/로드 (JSON)
- 곡별 기록 관리
"""

import json
import hashlib
from pathlib import Path
from typing import Optional, Dict
from datetime import datetime


class ScoreManager:
    """
    점수 관리 클래스

    OOP 원칙:
    - 단일 책임: 점수 계산 및 하이스코어 관리만 담당
    - 캡슐화: 점수 계산 로직 내부 은닉
    - 파일 I/O 캡슐화: 저장/로드 로직 내부화
    """

    # 점수 계산 상수
    BASE_SCORE_PER_OBSTACLE = 10
    PERFECT_DODGE_BONUS = 5
    COMBO_MULTIPLIER_BASE = 0.1  # 콤보 1당 10% 추가
    MAX_COMBO_MULTIPLIER = 3.0   # 최대 3배

    # 난이도 배율
    DIFFICULTY_MULTIPLIERS = {
        'easy': 1.0,
        'normal': 1.5,
        'hard': 2.0,
        'expert': 2.5
    }

    # 저장 경로
    SCORES_DIR = Path("data/scores")

    def __init__(self):
        """ScoreManager 초기화"""
        # 저장 디렉토리 생성
        self.SCORES_DIR.mkdir(parents=True, exist_ok=True)

        # 현재 세션 점수
        self._current_score = 0
        self._current_difficulty_multiplier = 1.0

    # ============================================================
    # Public Methods - 점수 계산
    # ============================================================

    def calculate_score(
        self,
        obstacles_avoided: int,
        perfect_dodges: int = 0,
        current_combo: int = 0,
        accuracy: float = 1.0
    ) -> int:
        """
        점수 계산

        Args:
            obstacles_avoided: 회피한 장애물 수
            perfect_dodges: 완벽한 회피 횟수
            current_combo: 현재 콤보 수
            accuracy: 정확도 (0.0~1.0)

        Returns:
            계산된 점수
        """
        # 기본 점수
        base_score = obstacles_avoided * self.BASE_SCORE_PER_OBSTACLE

        # 완벽한 회피 보너스
        perfect_bonus = perfect_dodges * self.PERFECT_DODGE_BONUS

        # 콤보 배율 계산
        combo_multiplier = self._calculate_combo_multiplier(current_combo)

        # 정확도 적용
        accuracy_factor = max(0.5, min(1.0, accuracy))

        # 최종 점수 = (기본 + 보너스) * 콤보 배율 * 정확도
        total_score = int((base_score + perfect_bonus) * combo_multiplier * accuracy_factor)

        return total_score

    def apply_difficulty_multiplier(
        self,
        base_score: int,
        difficulty_level: str
    ) -> int:
        """
        난이도 배율 적용

        Args:
            base_score: 기본 점수
            difficulty_level: 난이도 ('easy', 'normal', 'hard', 'expert')

        Returns:
            배율 적용된 최종 점수
        """
        multiplier = self.DIFFICULTY_MULTIPLIERS.get(
            difficulty_level.lower(),
            1.0
        )

        self._current_difficulty_multiplier = multiplier
        final_score = int(base_score * multiplier)

        return final_score

    def calculate_final_score(
        self,
        obstacles_avoided: int,
        perfect_dodges: int,
        max_combo: int,
        accuracy: float,
        difficulty_level: str
    ) -> Dict:
        """
        최종 점수 계산 (모든 요소 포함)

        Args:
            obstacles_avoided: 회피한 장애물 수
            perfect_dodges: 완벽한 회피 횟수
            max_combo: 최대 콤보 수
            accuracy: 정확도
            difficulty_level: 난이도

        Returns:
            점수 상세 정보 딕셔너리
        """
        # 기본 점수 계산
        base_score = self.calculate_score(
            obstacles_avoided,
            perfect_dodges,
            max_combo,
            accuracy
        )

        # 난이도 배율 적용
        final_score = self.apply_difficulty_multiplier(
            base_score,
            difficulty_level
        )

        self._current_score = final_score

        return {
            'base_score': base_score,
            'difficulty_multiplier': self._current_difficulty_multiplier,
            'final_score': final_score,
            'obstacles_avoided': obstacles_avoided,
            'perfect_dodges': perfect_dodges,
            'max_combo': max_combo,
            'accuracy': accuracy,
            'difficulty': difficulty_level
        }

    # ============================================================
    # Public Methods - 하이스코어 관리
    # ============================================================

    def save_high_score(
        self,
        song_id: str,
        score: int,
        statistics: Optional[Dict] = None
    ) -> bool:
        """
        하이스코어 저장

        Args:
            song_id: 곡 식별자 (파일명 또는 해시)
            score: 점수
            statistics: 추가 통계 정보 (선택)

        Returns:
            저장 성공 여부
        """
        try:
            # 곡 해시 생성 (파일 경로 안전화)
            song_hash = self._generate_song_hash(song_id)
            score_file = self.SCORES_DIR / f"{song_hash}.json"

            # 기존 기록 로드
            existing_data = self._load_score_file(score_file)

            # 새 기록 생성
            new_record = {
                'score': score,
                'timestamp': datetime.now().isoformat(),
                'statistics': statistics or {}
            }

            # 하이스코어 업데이트
            if 'high_score' not in existing_data or score > existing_data['high_score']['score']:
                existing_data['high_score'] = new_record

            # 플레이 기록 추가
            if 'play_history' not in existing_data:
                existing_data['play_history'] = []
            existing_data['play_history'].append(new_record)

            # 최근 10개만 유지
            existing_data['play_history'] = existing_data['play_history'][-10:]

            # 저장
            with open(score_file, 'w', encoding='utf-8') as f:
                json.dump(existing_data, f, indent=2, ensure_ascii=False)

            return True

        except Exception as e:
            print(f"[ERROR] Failed to save high score: {e}")
            return False

    def get_high_score(self, song_id: str) -> Optional[Dict]:
        """
        하이스코어 조회

        Args:
            song_id: 곡 식별자

        Returns:
            하이스코어 정보 (없으면 None)
        """
        try:
            song_hash = self._generate_song_hash(song_id)
            score_file = self.SCORES_DIR / f"{song_hash}.json"

            if not score_file.exists():
                return None

            data = self._load_score_file(score_file)
            return data.get('high_score')

        except Exception as e:
            print(f"[ERROR] Failed to load high score: {e}")
            return None

    def get_play_history(self, song_id: str, limit: int = 10) -> list:
        """
        플레이 기록 조회

        Args:
            song_id: 곡 식별자
            limit: 반환할 최대 기록 수

        Returns:
            플레이 기록 리스트 (최신순)
        """
        try:
            song_hash = self._generate_song_hash(song_id)
            score_file = self.SCORES_DIR / f"{song_hash}.json"

            if not score_file.exists():
                return []

            data = self._load_score_file(score_file)
            history = data.get('play_history', [])

            # 최신순으로 정렬
            history.reverse()
            return history[:limit]

        except Exception as e:
            print(f"[ERROR] Failed to load play history: {e}")
            return []

    # ============================================================
    # Private Methods - 내부 헬퍼
    # ============================================================

    def _calculate_combo_multiplier(self, combo: int) -> float:
        """
        콤보 배율 계산 (private)

        Args:
            combo: 콤보 수

        Returns:
            배율 (1.0 ~ MAX_COMBO_MULTIPLIER)
        """
        multiplier = 1.0 + (combo * self.COMBO_MULTIPLIER_BASE)
        return min(multiplier, self.MAX_COMBO_MULTIPLIER)

    def _generate_song_hash(self, song_id: str) -> str:
        """
        곡 ID를 파일명 안전한 해시로 변환 (private)

        Args:
            song_id: 곡 식별자

        Returns:
            SHA256 해시 (앞 16자)
        """
        hash_obj = hashlib.sha256(song_id.encode('utf-8'))
        return hash_obj.hexdigest()[:16]

    def _load_score_file(self, file_path: Path) -> Dict:
        """
        점수 파일 로드 (private)

        Args:
            file_path: 파일 경로

        Returns:
            점수 데이터 딕셔너리
        """
        if not file_path.exists():
            return {}

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            # 손상된 파일 → 빈 데이터 반환
            return {}

    # ============================================================
    # Getters
    # ============================================================

    @property
    def current_score(self) -> int:
        """현재 점수 (읽기 전용)"""
        return self._current_score

    @property
    def current_difficulty_multiplier(self) -> float:
        """현재 난이도 배율 (읽기 전용)"""
        return self._current_difficulty_multiplier

    def get_score_breakdown(self) -> Dict:
        """
        점수 상세 내역

        Returns:
            점수 구성 요소 딕셔너리
        """
        return {
            'current_score': self._current_score,
            'difficulty_multiplier': self._current_difficulty_multiplier,
            'base_score_per_obstacle': self.BASE_SCORE_PER_OBSTACLE,
            'perfect_bonus': self.PERFECT_DODGE_BONUS
        }
