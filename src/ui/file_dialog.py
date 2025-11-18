"""
FileDialog 클래스
파일 선택 다이얼로그 UI
"""

import tkinter as tk
from tkinter import filedialog
from typing import Optional


class FileDialog:
    """
    파일 선택 다이얼로그를 제공하는 클래스

    책임:
    - 사용자로부터 오디오 파일 경로 선택받기
    - 지원하는 파일 포맷 필터링
    """

    # 지원하는 파일 타입
    AUDIO_FILE_TYPES = [
        ("All Audio Files", "*.mp3 *.wav *.flac *.ogg"),
        ("MP3 Files", "*.mp3"),
        ("WAV Files", "*.wav"),
        ("FLAC Files", "*.flac"),
        ("OGG Files", "*.ogg"),
        ("All Files", "*.*")
    ]

    def __init__(self):
        """FileDialog 초기화"""
        # tkinter 루트 창 생성 (숨김)
        self._root = None

    def select_audio_file(self, title: str = "음악 파일 선택") -> Optional[str]:
        """
        오디오 파일 선택 다이얼로그 표시

        Args:
            title: 다이얼로그 제목

        Returns:
            선택된 파일 경로 (취소 시 None)
        """
        # tkinter 루트 창 초기화 (보이지 않게)
        self._init_root()

        # 파일 선택 다이얼로그 표시
        file_path = filedialog.askopenfilename(
            title=title,
            filetypes=self.AUDIO_FILE_TYPES
        )

        # 창 정리
        self._cleanup_root()

        # 빈 문자열이면 None 반환 (취소 시)
        return file_path if file_path else None

    def select_multiple_audio_files(self, title: str = "음악 파일 선택 (다중)") -> list:
        """
        여러 오디오 파일 선택 다이얼로그 표시

        Args:
            title: 다이얼로그 제목

        Returns:
            선택된 파일 경로 리스트 (취소 시 빈 리스트)
        """
        self._init_root()

        file_paths = filedialog.askopenfilenames(
            title=title,
            filetypes=self.AUDIO_FILE_TYPES
        )

        self._cleanup_root()

        return list(file_paths) if file_paths else []

    def _init_root(self) -> None:
        """
        tkinter 루트 창 초기화 (private 메서드)
        """
        if self._root is None:
            self._root = tk.Tk()
            self._root.withdraw()  # 메인 창 숨기기

    def _cleanup_root(self) -> None:
        """
        tkinter 루트 창 정리 (private 메서드)
        """
        if self._root:
            self._root.destroy()
            self._root = None


class LoadingScreen:
    """
    로딩 화면을 표시하는 클래스
    (Phase 1에서는 콘솔 출력만 지원, 추후 GUI 추가)
    """

    def __init__(self):
        """LoadingScreen 초기화"""
        self._is_loading = False

    def show(self, message: str = "분석 중...") -> None:
        """
        로딩 메시지 표시

        Args:
            message: 표시할 메시지
        """
        self._is_loading = True
        print(f"\n{'='*50}")
        print(f"  {message}")
        print(f"{'='*50}\n")

    def update(self, progress: float, message: str = "") -> None:
        """
        로딩 진행률 업데이트

        Args:
            progress: 진행률 (0.0 ~ 1.0)
            message: 진행 메시지
        """
        if not self._is_loading:
            return

        # 진행률 바 생성
        bar_length = 40
        filled_length = int(bar_length * progress)
        bar = '█' * filled_length + '-' * (bar_length - filled_length)

        # 진행률 출력
        print(f"\r진행률: [{bar}] {progress*100:.1f}% {message}", end='', flush=True)

    def hide(self) -> None:
        """로딩 화면 숨기기"""
        if self._is_loading:
            print("\n")  # 줄바꿈
            self._is_loading = False

    @property
    def is_loading(self) -> bool:
        """로딩 중 여부"""
        return self._is_loading
