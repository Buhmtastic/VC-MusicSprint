"""
Phase 2 데모 스크립트
코스 생성 시스템 테스트
"""

import sys
from pathlib import Path
import numpy as np

# 프로젝트 루트를 경로에 추가
sys.path.insert(0, str(Path(__file__).parent))

from src.audio.audio_analyzer import AudioAnalyzer
from src.course.course_generator import CourseGenerator
from src.course.visualizer import CourseVisualizer


def main():
    """Phase 2 데모 실행"""
    print("\n" + "="*70)
    print("  🎵 Music Sprint - Phase 2 데모")
    print("  코스 생성 시스템 테스트")
    print("="*70 + "\n")

    # 1. 더미 오디오 생성
    print("1️⃣  더미 오디오 데이터 생성 중...")
    sample_rate = 22050
    duration = 5.0
    frequency = 440.0

    t = np.linspace(0, duration, int(sample_rate * duration))

    # 비트감 있는 사인파 (엔벨로프 추가)
    envelope = 0.5 + 0.5 * np.sin(2 * np.pi * 3 * t)  # 3Hz 모듈레이션
    waveform = envelope * np.sin(2 * np.pi * frequency * t)

    print(f"   ✅ 생성 완료: {duration}초, {frequency}Hz")

    # 2. 오디오 분석
    print("\n2️⃣  오디오 분석 중...")
    analyzer = AudioAnalyzer()
    features = analyzer.analyze(waveform, sample_rate)

    print(f"   ✅ 분석 완료:")
    print(f"      - 총 길이: {features['duration']:.2f}초")
    print(f"      - 비트 개수: {features['beats']['count']}개")
    print(f"      - 템포: {features['tempo']['bpm']:.1f} BPM")
    print(f"      - 난이도: {features['difficulty']['level']} ({features['difficulty']['score']:.1f}/100)")

    # 3. 코스 생성
    print("\n3️⃣  코스 생성 중...")
    generator = CourseGenerator(seed=42)
    course = generator.generate(features, course_name="Demo Course - 440Hz")

    stats = course.get_statistics()
    print(f"   ✅ 코스 생성 완료:")
    print(f"      - 총 장애물: {stats['total_obstacles']}개")
    print(f"      - Beat 장애물: {stats['by_type']['beat']}개")
    print(f"      - Frequency 장애물: {stats['by_type']['frequency']}개")
    print(f"      - Amplitude 장애물: {stats['by_type']['amplitude']}개")
    print(f"      - 밀도: {stats['density']:.2f} obstacles/sec")

    # 4. 코스 시각화
    print("\n4️⃣  코스 시각화 중...")
    visualizer = CourseVisualizer()

    output_path = "assets/phase2_demo_course.png"
    visualizer.visualize(course, output_path=output_path, show=False)

    print(f"   ✅ 시각화 저장: {output_path}")

    # 5. 장애물 샘플 출력
    print("\n5️⃣  장애물 샘플 (처음 10개):")
    print("   " + "-"*66)
    print(f"   {'Time':>8} | {'Type':^12} | {'Height':>8} | {'Color':^15}")
    print("   " + "-"*66)

    for i, obstacle in enumerate(course.obstacles[:10]):
        info = obstacle.get_info()
        print(f"   {info['time']:>8.2f}s | {info['type']:^12} | "
              f"{info['height']:>8.1f} | {str(info['color']):^15}")

    if course.obstacle_count > 10:
        print(f"   ... (총 {course.obstacle_count}개)")
    print("   " + "-"*66)

    # 6. 다형성 데모
    print("\n6️⃣  다형성 테스트:")
    print("   모든 Obstacle 타입을 동일한 방식으로 처리 가능")

    sample_obstacles = course.obstacles[:5]
    for obs in sample_obstacles:
        # 모든 Obstacle은 동일한 인터페이스 제공
        print(f"   - {obs.get_type().value:12} @ {obs.time:.2f}s: "
              f"height={obs.get_height():.1f}, color={obs.get_color()}")

    # 완료
    print("\n" + "="*70)
    print("  ✅ Phase 2 데모 완료!")
    print("  다음 단계: Phase 3 (캐릭터 및 자동 플레이)")
    print("="*70 + "\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ 에러 발생: {e}")
        import traceback
        traceback.print_exc()
