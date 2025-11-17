# Music Sprint 게임 개발 기획서

## 프로젝트 개요

**게임명**: Music Sprint (뮤직 스프린트)  
**장르**: 음악 기반 방치형 러너 (Music-Driven Idle Runner)  
**플랫폼**: PC (Python/PyGame) → 모바일 확장 (추후)  
**개발 기간**: 8~10주 (MVP 5주 + 수익화 2주 + API 연동 2주 + 버퍼 1주)  
**개발 목적**: 포트폴리오 + 수익 창출형 게임 개발 프로젝트  
**개발 방법론**: **객체지향 프로그래밍(OOP) 원칙 엄격 준수** ⚠️  
**비즈니스 모델**: Freemium + 프리미엄 구독 + 스킨 판매

**컨셉**: 사용자가 업로드한 음원의 파형(Waveform)을 실시간 분석하여 자동으로 코스를 생성하고, 캐릭터가 음악에 맞춰 자동으로 달리는 방치형 러너 게임. 음악이 끝나면 점수와 통계를 제공하며, 다양한 음악 플랫폼(Spotify, 벅스, 멜론, Suno)과 연동 가능.

---

## ⚠️ 필수 개발 원칙: 객체지향 프로그래밍 (OOP)

### 중요도: 🔴 CRITICAL - 준수하지 않으면 프로젝트 실패

본 프로젝트는 **객체지향 프로그래밍(OOP) 원칙을 엄격히 준수**하여 개발해야 합니다.

**이유**:
- 복잡한 음원 분석 로직을 모듈화
- 확장 가능한 구조 (새로운 음악 플랫폼 추가)
- 유지보수 용이성 (1인 개발자)
- 전문적인 개발 역량 증명
- 수익 창출 기능 추가 시 확장성

**적용 원칙**:
1. ✅ **캡슐화(Encapsulation)**: 음원 분석, 코스 생성 로직을 클래스 내부에 은닉
2. ✅ **상속(Inheritance)**: 음악 플랫폼별 연동 클래스를 부모 클래스로 추상화
3. ✅ **다형성(Polymorphism)**: 다양한 음원 포맷을 동일 인터페이스로 처리
4. ✅ **추상화(Abstraction)**: 복잡한 FFT 분석 알고리즘을 인터페이스로 숨김

**SOLID 원칙**:
- **S**ingle Responsibility: AudioAnalyzer는 분석만, CourseGenerator는 생성만
- **O**pen/Closed: 새 음악 플랫폼 추가 시 기존 코드 수정 불필요
- **L**iskov Substitution: 모든 MusicProvider는 동일하게 동작
- **I**nterface Segregation: 각 인터페이스는 최소한의 메서드만
- **D**ependency Inversion: Game이 구체적 분석기가 아닌 추상화에 의존

---

## 1. 개발 목적

### 기술적 목적
- **음원 신호 처리 학습**: Librosa, NumPy를 활용한 오디오 분석 (FFT, Beat Detection, Amplitude Envelope)
- **실시간 데이터 처리**: 음원 파형을 실시간으로 게임 요소로 변환하는 파이프라인 구축
- **API 연동 경험**: Spotify, 벅스, 멜론 등 외부 음악 플랫폼 API 통합
- **OOP 심화 학습**: 복잡한 시스템을 객체지향으로 설계 및 구현
- **알고리즘 최적화**: 대용량 음원 파일 처리 시 성능 최적화

### 비즈니스 목적
- **수익 창출**: 1인 개발자로서 실제 수익을 낼 수 있는 게임 개발
- **포트폴리오 강화**: 기술력 + 비즈니스 감각을 동시에 보여주는 프로젝트
- **음악 생태계 연계**: 음악 스트리밍 서비스와의 파트너십 가능성 탐색
- **커뮤니티 구축**: 음악 애호가들의 커뮤니티 형성
- **확장 가능한 플랫폼**: 모바일, 웹으로 확장 가능한 기반 마련

### 차별화 포인트
- **음악이 곧 게임**: 단순 배경음악이 아닌, 음악 자체가 게임 콘텐츠
- **무한 콘텐츠**: 사용자의 음악 라이브러리가 게임 콘텐츠
- **방치형 + 음악**: 방치형 게임의 편안함 + 음악 감상의 즐거움
- **소셜 기능**: 같은 곡으로 경쟁하고 기록을 공유

---

## 2. 게임 메커니즘

### 2.1 핵심 게임플레이

#### 음원 업로드 및 분석
1. **음원 선택**:
   - 로컬 파일 업로드 (.mp3, .wav, .flac 지원)
   - Spotify 연동 (플레이리스트 가져오기)
   - 벅스/멜론 연동 (추후)
   - Suno AI 생성 곡 연동

2. **파형 분석** (AudioAnalyzer):
   ```
   음원 → FFT 분석 → 주파수 대역 추출
        → Beat Detection → 비트 타이밍
        → Amplitude Envelope → 볼륨 변화
        → Spectral Centroid → 음색 분석
   ```

3. **코스 생성** (CourseGenerator):
   ```
   파형 데이터 → 장애물 배치 알고리즘
              → 높이 변화 (고음 = 높은 장애물)
              → 밀도 조절 (비트 = 장애물 등장)
              → 색상 변화 (주파수 = 배경색)
   ```

#### 게임 진행 (방치형)
- **자동 달리기**: 캐릭터가 코스를 자동으로 달림
- **자동 점프/회피**: 음악 비트에 맞춰 자동으로 장애물 회피
- **시각적 피드백**: 음악 파형이 실시간으로 배경에 표시
- **점수 계산**: 
  - 기본 점수: 거리 × 음악 길이
  - 보너스: 퍼펙트 회피(비트 정확도), 콤보
  - 난이도 배율: 곡의 복잡도에 따라 배율 적용

#### 게임 종료
- 음악이 끝나면 자동 종료
- 결과 화면:
  - 최종 점수
  - 통계 (정확도, 콤보, 거리)
  - 랭킹 (같은 곡을 플레이한 다른 유저 대비)
  - 공유 기능 (소셜 미디어)

### 2.2 주요 기능

#### 필수 기능 (MVP)
- [ ] 로컬 음원 파일 업로드 (.mp3, .wav)
- [ ] 음원 파형 실시간 분석
- [ ] 파형 기반 코스 자동 생성
- [ ] 캐릭터 자동 달리기 및 회피
- [ ] 점수 및 통계 시스템
- [ ] 로컬 하이스코어 저장

#### 확장 기능 (Post-MVP)
- [ ] Spotify API 연동
- [ ] 온라인 리더보드
- [ ] 캐릭터 커스터마이징 (스킨 구매)
- [ ] 소셜 공유 기능
- [ ] 벅스/멜론 API 연동
- [ ] Suno AI 곡 자동 가져오기
- [ ] 멀티플레이어 (같은 곡으로 경쟁)

### 2.3 제공 가치

**플레이어 가치**:
- **음악 감상의 새로운 경험**: 단순 듣기가 아닌 시각화된 음악 체험
- **방치형의 편안함**: 적극적 조작 없이 음악 감상 + 게임
- **개인화된 콘텐츠**: 내 음악 라이브러리가 게임 콘텐츠
- **소셜 경쟁**: 친구들과 같은 곡으로 점수 경쟁
- **음악 발견**: 다른 유저들이 플레이한 곡 추천

**개발자 가치**:
- **수익 창출**: 광고, 프리미엄 기능, 제휴 수익
- **포트폴리오**: 복잡한 시스템 설계 및 구현 능력 증명
- **확장성**: 모바일, 웹, VR로 확장 가능

---

## 3. 수익 창출 모델 (1인 개발자 최적화)

### 💰 비즈니스 모델: Freemium + 광고 + 제휴

#### 3.1 무료 버전 (Free Tier)
**목표**: 사용자 유입 최대화

**제공 기능**:
- ✅ 로컬 음원 파일 업로드 (1일 5곡 제한)
- ✅ 기본 캐릭터 1종
- ✅ 로컬 하이스코어
- ⚠️ 프리미엄 기능 제한 (Spotify 연동, 스킨, 온라인 리더보드)

**수익 전략**:
- PC 버전은 **광고 없이 시작** (기술적 복잡성 및 낮은 수익률)
- **프리미엄 전환 유도**에 집중
- 모바일 앱 출시 후 Google AdMob 통합 예정

#### 3.2 프리미엄 버전 (Premium Tier)
**가격**: $2.99 / 월 또는 $19.99 / 연 (70% 할인)

**제공 기능**:
- ✅ **무제한 곡 업로드**
- ✅ **광고 제거**
- ✅ **캐릭터 스킨 10종 무료**
- ✅ **Spotify 연동** (플레이리스트 자동 동기화)
- ✅ **온라인 글로벌 리더보드**
- ✅ **고음질 분석** (더 정확한 코스 생성)
- ✅ **곡 공유 및 추천 기능**

**예상 수익**:
- 전환율 1~2% 가정: 500 DAU → 5~10명 구독 (초기 현실적 목표)
- 월 수익: 5~10명 × $2.99 = **$15~30/월** (초기)
- 1,000 DAU 도달 시: 10~20명 → **$30~60/월**
- 연 수익: **$180~720/년** (1인 개발자 부수입 수준)

#### 3.3 캐릭터 스킨 판매 (In-App Purchase)
**가격**: $0.99 ~ $2.99 / 스킨

**스킨 종류**:
- 기본: 러너 (무료)
- 프리미엄: 음악 아이콘 (기타, 드럼, 마이크 등) - $0.99
- 레어: 유명 아티스트 협업 (라이센스 필요) - $2.99
- 커스텀: 사용자 이미지 업로드 → 커스텀 스킨 - $1.99

**예상 수익**:
- 월 20~50건 구매 가정 (초기 3~5% 구매율)
- 평균 $1.50 × 35건 = **$50/월** (초기 목표)

#### 3.4 음악 스트리밍 서비스 제휴 (장기 전략)

##### A. Spotify 연동 (기능적 통합)
**모델**: Spotify API 통합 → 프리미엄 전환율 향상

**구조**:
1. **사용자가 Spotify 계정으로 로그인**
2. **플레이리스트 자동 가져오기** (편의성 증대)
3. **30초 미리듣기 지원** (Spotify API 약관 준수)
4. **프리미엄 기능**으로 제공 → 전환 유도

**실현 방법**:
- Spotify Developer Program 가입
- Spotify Web API 통합
- OAuth 2.0 인증 구현
- "Spotify로 플레이" 기능 추가

**예상 효과** (간접 수익):
- Spotify 연동으로 **프리미엄 전환율 +30~50% 상승**
- 기존 전환율 1% → 1.3~1.5% 향상
- 월 추가 구독: 2~5명 → **+$6~15/월** (간접 효과)

**중요**: Spotify는 앱 개발자에게 직접 수익을 분배하지 않음. 연동은 **사용자 경험 개선**을 위한 기능.

##### B. 벅스/멜론 연동 (한국 시장 진출)
**모델**: API 연동 → 한국 시장 진입 → 사용자 확보

**구조**:
1. **벅스/멜론 API 통합** (API 제공 여부 확인 필요)
2. 한국 음악 라이브러리 접근
3. K-POP 팬층 확보

**실현 방법**:
- 벅스/멜론 API 공식 문서 확인
- API 제공 안 될 경우 → 로컬 파일 업로드로 대체
- 한국 커뮤니티 마케팅 (디시인사이드, 오늘의유머)

**예상 효과**:
- 한국 시장 진출 시 **유리한 포지션 확보**
- K-POP 팬 유입 (글로벌 시장)
- 직접 수익보다는 **사용자 기반 확대** 목표

**중요**: 벅스/멜론은 소규모 앱에 파트너십을 제공하지 않음. 초기에는 **기능적 통합**에만 집중.

##### C. Suno AI 연동 (선택적, 실험적)
**모델**: Suno 생성 곡 자동 연동 → 교차 프로모션

**구조**:
1. **Suno에서 곡 생성 → Music Sprint로 수동 업로드**
2. **Music Sprint에서 → "AI 음악 생성" 안내 링크**
3. **교차 프로모션**: 서로 사용자 유입 (파트너십 없이도 가능)

**실현 방법**:
- ⚠️ Suno는 **공식 API 없음** (2024년 기준)
- 공식 API 출시 대기 (로드맵 확인)
- 출시 전까지는 **수동 업로드 권장**
- 웹 스크래핑은 ToS 위반 위험 → **권장 안 함**

**예상 효과**:
- 직접 수익보다 **사용자 유입** 효과
- Suno 사용자 → Music Sprint 유입 (월 50~100명 예상)
- 간접 수익: **+$2~5/월** (매우 낮음)

**우선순위**: 🔴 낮음 (Spotify 연동이 우선)  
**성공 가능성**: 30% (공식 API 출시 불확실)

#### 3.5 커뮤니티 기능 (추후 수익화)

**기능**:
- 곡 공유 및 추천
- 친구 리더보드
- 주간 챌린지 (특정 곡으로 경쟁)

**수익화 방안**:
- 프리미엄 사용자만 무제한 공유
- 챌린지 참가권 (무료: 주 3회, 프리미엄: 무제한)

---

### 💵 수익 요약 (1년차 예상)

| 수익원 | 월 수익 | 연 수익 | 비고 |
|--------|---------|---------|------|
| **프리미엄 구독** | $15~60 | $180~720 | 500~1,000 DAU, 전환율 1~2% |
| **스킨 판매** | $50 | $600 | 월 35건 |
| **Spotify 간접 효과** | +$6~15 | +$72~180 | 전환율 향상 효과 |
| **Suno 간접 효과** | +$2~5 | +$24~60 | 유입 효과 (낮음) |
| **총계 (1년차)** | **$73~130** | **$876~1,560** | 보수적 추정 |

**📊 현실적 목표 (1인 개발자)**:
- **1~3개월**: $10~30/월 (구독만, 소수 얼리어답터)
- **4~6개월**: $50~80/월 (구독 + 스킨)
- **7~12개월**: $100~150/월 (Spotify 연동 후 전환율 상승)
- **2년차 목표**: $200~400/월 (모바일 확장, 광고 추가)

**시나리오별 분석**:

| 시나리오 | DAU | 전환율 | 월 수익 | 연 수익 |
|---------|-----|--------|---------|---------|
| **최악** | 100 | 0.5% | $20~40 | $240~480 |
| **보통** | 500 | 1% | $70~100 | $840~1,200 |
| **좋음** | 1,000 | 2% | $130~180 | $1,560~2,160 |
| **최상** | 2,000 | 2.5% | $250~350 | $3,000~4,200 |

**중요**: 
- 초기 목표는 **"보통" 시나리오** ($70~100/월)
- 모바일 앱 출시 후 AdMob 추가 시 **2~3배 증가 가능**
- Spotify/벅스 **공식 파트너십은 비현실적** (간접 효과만 기대)

---

## 4. 개발 단계별 마일스톤 (8~10주)

**총 소요 시간**: 약 100~120시간 (주당 10~15시간, 1인 개발자 현실적 목표)

### Phase 1: 프로토타입 및 음원 분석 (1~1.5주)

#### 작업 항목
- [ ] 프로젝트 구조 생성
- [ ] `AudioAnalyzer` 클래스 구현 ⭐ **OOP + 알고리즘**
  - [ ] Librosa 기반 파형 분석
  - [ ] FFT (Fast Fourier Transform) 구현
  - [ ] Beat Detection (비트 감지)
  - [ ] Amplitude Envelope (볼륨 변화)
  - [ ] Private 메서드: _extract_features()
- [ ] `AudioLoader` 클래스 ⭐ **OOP - 단일 책임**
  - [ ] 로컬 파일 로드 (.mp3, .wav)
  - [ ] 파일 포맷 검증
  - [ ] 에러 처리 (손상된 파일, 지원 안 되는 포맷)
- [ ] 기본 UI
  - [ ] 파일 선택 다이얼로그
  - [ ] 로딩 화면 (분석 중...)
- [ ] 테스트: 샘플 음원 3곡으로 파형 분석 검증

#### OOP 체크리스트
- [ ] **캡슐화**: AudioAnalyzer의 _waveform_data private
- [ ] **단일 책임**: AudioLoader는 로드만, Analyzer는 분석만
- [ ] **에러 처리**: 파일 로드 실패 시 graceful degradation

#### Definition of Done
- ✅ mp3 파일 로드 성공
- ✅ 파형 데이터 추출 (amplitude, beat positions)
- ✅ 콘솔에 분석 결과 출력 (비트 개수, 평균 볼륨)
- ✅ 3개 샘플 곡 테스트 완료

#### 예상 소요 시간
- Librosa 학습 및 설치: 2시간
- AudioLoader 클래스: 2시간
- AudioAnalyzer 클래스: 4시간
- 테스트 및 디버깅: 2시간
**총 10시간**

---

### Phase 2: 코스 생성 시스템 (1.5~2주)

#### 작업 항목
- [ ] `CourseGenerator` 클래스 ⭐ **OOP - Factory Pattern**
  - [ ] generate(audio_data) 메서드
  - [ ] _create_obstacles_from_beats() private
  - [ ] _create_height_from_frequency() private
  - [ ] _create_background_from_spectral() private
- [ ] `Obstacle` 클래스 계층 구조 ⭐ **OOP - 상속**
  - [ ] Obstacle (추상 부모)
  - [ ] BeatObstacle (비트 기반)
  - [ ] FrequencyWall (주파수 기반)
  - [ ] AmplitudeGap (볼륨 기반)
- [ ] `Course` 클래스 ⭐ **OOP - 캡슐화**
  - [ ] _obstacles 리스트 (private)
  - [ ] _timeline 딕셔너리 {time: [obstacles]}
  - [ ] get_obstacles_at_time(t) 메서드
- [ ] 알고리즘 구현
  - [ ] 비트 → 장애물 위치 매핑
  - [ ] 주파수 → 장애물 높이 매핑
  - [ ] 볼륨 → 장애물 밀도 매핑
- [ ] 시각화 테스트
  - [ ] 생성된 코스를 정적 이미지로 출력
  - [ ] 음원과 코스 비교 검증

#### OOP 체크리스트
- [ ] **Factory Pattern**: CourseGenerator가 음원 데이터로 코스 객체 생성
- [ ] **상속**: 모든 Obstacle이 공통 인터페이스 구현
- [ ] **캡슐화**: Course의 내부 데이터 직접 접근 불가
- [ ] **다형성**: 다양한 Obstacle 타입을 동일하게 처리

#### Definition of Done
- ✅ 음원 데이터 → Course 객체 변환 성공
- ✅ 비트마다 장애물 생성됨
- ✅ 주파수에 따라 장애물 높이 변화
- ✅ 정적 코스 이미지 생성 및 검증
- ✅ 3개 서로 다른 곡으로 다른 코스 생성 확인

#### 예상 소요 시간
- CourseGenerator 설계: 2시간
- Obstacle 클래스 계층: 3시간
- 매핑 알고리즘 구현: 4시간
- 시각화 및 검증: 3시간
**총 12시간**

---

### Phase 3: 캐릭터 및 자동 플레이 (1.5~2주)

#### 작업 항목
- [ ] `Character` 클래스 ⭐ **OOP**
  - [ ] Private 속성: _x, _y, _velocity
  - [ ] auto_jump(beat_time) 메서드
  - [ ] auto_duck(frequency) 메서드
  - [ ] update(delta_time) 메서드
- [ ] `AutoPlayController` 클래스 ⭐ **OOP - Strategy Pattern**
  - [ ] decide_action(obstacle, character) 메서드
  - [ ] 장애물 종류에 따라 자동 판단 (점프/숙이기/아무것도 안 함)
- [ ] `Game` 클래스 메인 루프
  - [ ] 음악 재생과 게임 동기화
  - [ ] 현재 시간(t)에 맞는 장애물 가져오기
  - [ ] 충돌 감지
  - [ ] 점수 계산
- [ ] 애니메이션
  - [ ] 캐릭터 달리기 (2~3 프레임)
  - [ ] 점프 애니메이션
  - [ ] 숙이기 애니메이션
- [ ] 파형 배경 렌더링
  - [ ] 실시간으로 음원 파형 표시
  - [ ] 주파수별 색상 변화

#### OOP 체크리스트
- [ ] **Strategy Pattern**: AutoPlayController가 상황별 전략 결정
- [ ] **캡슐화**: Character 내부 상태 외부 접근 불가
- [ ] **단일 책임**: Game은 조율만, AutoPlay는 판단만
- [ ] **시간 동기화**: 음악 타이머와 게임 루프 정확히 일치

#### Definition of Done
- ✅ 캐릭터가 자동으로 달림
- ✅ 비트에 맞춰 자동 점프
- ✅ 장애물 회피 성공률 80% 이상
- ✅ 음악 재생과 게임 동기화 (오차 ±50ms)
- ✅ 파형이 배경에 실시간 표시
- ✅ 음악 끝나면 자동 종료

#### 예상 소요 시간
- Character 클래스: 3시간
- AutoPlayController: 4시간
- Game 루프 동기화: 3시간
- 애니메이션: 2시간
- 파형 렌더링: 2시간
**총 14시간**

---

### Phase 4: 점수 및 결과 시스템 (1주)

#### 작업 항목
- [ ] `ScoreManager` 클래스 ⭐ **OOP - 단일 책임**
  - [ ] calculate_score(distance, accuracy, combo)
  - [ ] apply_difficulty_multiplier(song_complexity)
  - [ ] save_high_score(song_id, score)
  - [ ] get_high_score(song_id)
- [ ] `StatisticsTracker` 클래스 ⭐ **OOP**
  - [ ] track_jump(is_perfect: bool)
  - [ ] track_combo(current_combo)
  - [ ] get_summary() → 딕셔너리 반환
- [ ] 결과 화면 UI
  - [ ] 최종 점수
  - [ ] 정확도 그래프
  - [ ] 콤보 기록
  - [ ] 하이스코어 비교
- [ ] 로컬 데이터 저장
  - [ ] JSON 형식으로 곡별 기록 저장
  - [ ] 파일 경로: `data/scores/{song_hash}.json`
- [ ] 곡 난이도 분석
  - [ ] BPM, 주파수 분산, 비트 밀도로 난이도 계산
  - [ ] 난이도에 따라 점수 배율 적용

#### OOP 체크리스트
- [ ] **단일 책임**: ScoreManager는 점수만, Tracker는 통계만
- [ ] **캡슐화**: 점수 계산 로직 외부 노출 안 됨
- [ ] **파일 I/O 캡슐화**: 저장/로드 로직이 Manager 내부에
- [ ] **에러 처리**: 파일 없을 때 기본값 반환

#### Definition of Done
- ✅ 게임 종료 시 점수 계산 정확
- ✅ 난이도 배율이 적용됨 (Easy 1.0x, Hard 2.0x)
- ✅ 결과 화면이 표시됨
- ✅ 하이스코어가 로컬에 저장됨
- ✅ 같은 곡 재플레이 시 이전 기록 표시

#### 예상 소요 시간
- ScoreManager: 3시간
- StatisticsTracker: 2시간
- 결과 화면 UI: 3시간
- 난이도 분석: 2시간
- 저장/로드: 2시간
**총 12시간**

---

### Phase 5: 프리미엄 및 수익화 시스템 (1.5~2주)

#### 작업 항목
- [ ] **프리미엄 기능 게이트**
  - [ ] 곡 업로드 제한 (무료: 5곡/일, 프리미엄: 무제한)
  - [ ] "프리미엄 구독하기" 버튼 → 웹 결제 페이지
  - [ ] 구독 상태 확인 (로컬 저장)
- [ ] **스킨 시스템**
  - [ ] `SkinManager` 클래스 ⭐ **OOP**
  - [ ] 기본 스킨 1개 무료 제공
  - [ ] 프리미엄 스킨 잠금 (구매 필요)
  - [ ] "스킨 구매" 버튼 → 결제 페이지
- [ ] **결제 연동** (최소 구현)
  - [ ] Stripe Checkout (웹 기반)
  - [ ] PayPal (웹 기반, 선택적)
  - [ ] 결제 완료 → 로컬에 구매 기록 저장
  - [ ] 서버 없이 작동 (초기 버전)
- [ ] **광고 시스템** (보류)
  - [ ] ⚠️ PC 버전은 광고 없이 시작
  - [ ] 모바일 앱 출시 후 Google AdMob 통합 예정
  - [ ] 기술적 복잡성 및 낮은 ROI로 우선순위 낮음

#### OOP 체크리스트
- [ ] **단일 책임**: PaymentManager는 결제만, SkinManager는 스킨만
- [ ] **Strategy Pattern**: 여러 결제 수단 동일 인터페이스
- [ ] **캡슐화**: 구매 기록이 외부 노출 안 됨
- [ ] **보안**: 로컬 결제 검증 (추후 서버 검증으로 업그레이드)

#### Definition of Done
- ✅ "프리미엄 구독" 버튼 클릭 → 웹 결제 페이지 열림
- ✅ 결제 완료 시 프리미엄 상태 활성화
- ✅ 스킨 구매 가능
- ✅ 무료 유저는 5곡/일 제한 적용

#### 예상 소요 시간
- 프리미엄 게이트: 3시간
- 스킨 시스템: 4시간
- 결제 연동: 5시간
- 테스트: 3시간
**총 15시간**

---

### Phase 6: 음악 플랫폼 연동 (2~2.5주)

#### 작업 항목
- [ ] **Spotify API 연동** ⭐ **최우선**
  - [ ] `SpotifyProvider` 클래스 ⭐ **OOP - MusicProvider 상속**
  - [ ] OAuth 2.0 인증 (Spotify Developer App 등록)
  - [ ] 플레이리스트 가져오기 (Get User's Playlists)
  - [ ] 트랙 메타데이터 가져오기
  - [ ] 음원 미리듣기 (30초 preview)
- [ ] **MusicProvider 추상 클래스** ⭐ **OOP - 추상화**
  - [ ] 공통 인터페이스: authenticate(), get_playlists(), get_track()
  - [ ] 하위 클래스: SpotifyProvider, LocalProvider
  - [ ] (SunoProvider는 선택적, 낮은 우선순위)
- [ ] **로컬 파일 + Spotify 통합**
  - [ ] "음원 선택" 화면에 탭 추가 (로컬 / Spotify)
  - [ ] Spotify 로그인 버튼
  - [ ] 플레이리스트 목록 표시
- [ ] **Suno 연동** (선택적, 시간 여유 시에만)
  - [ ] ⚠️ 우선순위: 낮음 (공식 API 없음)
  - [ ] 가능하면 "Suno로 곡 생성" 외부 링크만 추가
  - [ ] 자동 연동은 보류 (ToS 위반 위험)

#### OOP 체크리스트
- [ ] **추상화**: MusicProvider 인터페이스로 다양한 플랫폼 통합
- [ ] **다형성**: 모든 Provider를 동일하게 처리
- [ ] **개방-폐쇄**: 새 플랫폼 추가 시 기존 코드 수정 없음
- [ ] **의존성 역전**: Game이 구체적 Provider가 아닌 추상화에 의존

#### Definition of Done
- ✅ Spotify 로그인 성공
- ✅ 플레이리스트 가져오기 성공
- ✅ Spotify 곡으로 게임 플레이 가능 (30초 preview)
- ✅ 2개 플랫폼 테스트 (로컬, Spotify)
- ⚠️ Suno는 선택적 (시간 없으면 스킵)

#### 예상 소요 시간
- Spotify API 학습: 3시간
- SpotifyProvider 구현: 5시간
- MusicProvider 추상화: 2시간
- UI 통합: 4시간
- OAuth 디버깅: 3시간
- (Suno 연동: 3시간 - 선택적)
**총 17~20시간**

---

## 5. 기술 스택

### 개발 환경
- **언어**: Python 3.10+
- **게임 엔진**: PyGame 2.5+
- **IDE**: VS Code / PyCharm
- **버전 관리**: Git + GitHub

### 핵심 라이브러리
```python
# requirements.txt

# 게임 엔진
pygame==2.5.2

# 음원 분석
librosa==0.10.1
numpy==1.24.3
scipy==1.11.4

# 음악 플랫폼 API
spotipy==2.23.0        # Spotify API
requests==2.31.0       # HTTP 요청

# UI 및 웹뷰
pygame-gui==0.6.9      # GUI 위젯
cefpython3==66.1       # 웹뷰 (광고용)

# 데이터 저장
# json (기본 내장)

# 유틸리티
python-dotenv==1.0.0   # 환경 변수 관리
```

### 외부 API
- **Spotify Web API**: 플레이리스트, 트랙 메타데이터
- **Google AdMob**: 광고 (웹뷰 통합)
- **Stripe API**: 결제 처리
- **Suno (비공식)**: AI 생성 음악

### 개발 도구
- **Black/Pylint**: 코드 품질
- **pytest**: 단위 테스트
- **Librosa Visualizer**: 음원 분석 디버깅

---

## 6. 프로젝트 구조

```
musicsprint/
├── main.py                     # 게임 실행 진입점
├── game.py                     # Game 클래스 (메인 루프)
├── config.py                   # 게임 상수
├── audio/
│   ├── __init__.py
│   ├── audio_loader.py         # AudioLoader 클래스
│   ├── audio_analyzer.py       # AudioAnalyzer 클래스 (FFT, Beat Detection)
│   └── music_provider.py       # MusicProvider 추상 클래스
├── course/
│   ├── __init__.py
│   ├── course_generator.py     # CourseGenerator 클래스 (Factory)
│   ├── course.py               # Course 클래스
│   └── obstacles.py            # Obstacle 클래스 계층
├── character/
│   ├── __init__.py
│   ├── character.py            # Character 클래스
│   └── auto_play_controller.py # AutoPlayController (Strategy)
├── managers/
│   ├── __init__.py
│   ├── score_manager.py        # ScoreManager 클래스
│   ├── statistics_tracker.py   # StatisticsTracker 클래스
│   ├── skin_manager.py         # SkinManager 클래스
│   ├── payment_manager.py      # PaymentManager 클래스
│   └── ad_manager.py           # AdManager (모바일 버전용, PC에서는 미사용)
├── platforms/
│   ├── __init__.py
│   ├── spotify_provider.py     # SpotifyProvider (MusicProvider 상속)
│   ├── local_provider.py       # LocalProvider (기본 로컬 파일)
│   └── suno_provider.py        # SunoProvider (실험적)
├── ui/
│   ├── __init__.py
│   ├── menu_screen.py          # 메인 메뉴
│   ├── song_select_screen.py   # 곡 선택
│   ├── game_screen.py          # 게임 플레이
│   ├── result_screen.py        # 결과 화면
│   └── premium_screen.py       # 프리미엄 안내
├── assets/
│   ├── sprites/                # 캐릭터, 장애물 스프라이트
│   ├── fonts/                  # 폰트
│   └── sounds/                 # 효과음
├── data/
│   ├── scores/                 # 곡별 점수 (JSON)
│   └── user_data.json          # 사용자 프로필 (프리미엄 상태 등)
├── tests/
│   ├── test_audio_analyzer.py
│   ├── test_course_generator.py
│   └── test_score_manager.py
├── requirements.txt
├── README.md
├── LICENSE
└── .env                        # API 키 (Spotify, Stripe)
```

---

## 7. 핵심 클래스 설계 (OOP 원칙 적용)

### 7.1 AudioAnalyzer 클래스 (음원 분석)

```python
import librosa
import numpy as np

class AudioAnalyzer:
    """
    음원 파형 분석 클래스
    - FFT로 주파수 분석
    - Beat Detection으로 비트 감지
    - Amplitude Envelope로 볼륨 변화 추출
    """
    
    def __init__(self, audio_path):
        self._audio_path = audio_path     # private
        self._waveform = None             # private
        self._sample_rate = None          # private
        self._beats = []                  # private
        self._amplitudes = []             # private
        self._spectral_centroids = []    # private
    
    def analyze(self):
        """음원 분석 수행 (Public 인터페이스)"""
        self._load_audio()
        self._detect_beats()
        self._extract_amplitude()
        self._extract_spectral_features()
        return self._create_analysis_result()
    
    # Private 메서드 (내부 구현)
    def _load_audio(self):
        """음원 로드"""
        self._waveform, self._sample_rate = librosa.load(self._audio_path)
    
    def _detect_beats(self):
        """비트 감지 (Beat Detection)"""
        tempo, beat_frames = librosa.beat.beat_track(
            y=self._waveform, 
            sr=self._sample_rate
        )
        self._beats = librosa.frames_to_time(beat_frames, sr=self._sample_rate)
    
    def _extract_amplitude(self):
        """볼륨 변화 추출"""
        self._amplitudes = np.abs(self._waveform)
    
    def _extract_spectral_features(self):
        """스펙트럼 특징 추출 (주파수)"""
        spectral_centroids = librosa.feature.spectral_centroid(
            y=self._waveform, 
            sr=self._sample_rate
        )[0]
        self._spectral_centroids = spectral_centroids
    
    def _create_analysis_result(self):
        """분석 결과 딕셔너리 생성"""
        return {
            'beats': self._beats.tolist(),
            'amplitudes': self._amplitudes.tolist(),
            'spectral_centroids': self._spectral_centroids.tolist(),
            'duration': len(self._waveform) / self._sample_rate,
            'sample_rate': self._sample_rate
        }
    
    # Property (읽기 전용)
    @property
    def duration(self):
        """음원 길이 (초)"""
        if self._waveform is not None:
            return len(self._waveform) / self._sample_rate
        return 0
```

**OOP 원칙**:
- ✅ **캡슐화**: 모든 분석 데이터 private
- ✅ **단일 책임**: 음원 분석만 담당
- ✅ **명확한 인터페이스**: analyze() 하나로 간단히 사용

---

### 7.2 CourseGenerator 클래스 (Factory Pattern)

```python
class CourseGenerator:
    """
    음원 분석 데이터로 코스 생성 (Factory Pattern)
    - 비트 → 장애물 위치
    - 주파수 → 장애물 높이
    - 볼륨 → 장애물 밀도
    """
    
    def __init__(self, analyzer_result):
        self._beats = analyzer_result['beats']
        self._amplitudes = analyzer_result['amplitudes']
        self._spectral_centroids = analyzer_result['spectral_centroids']
        self._sample_rate = analyzer_result['sample_rate']
    
    def generate(self):
        """코스 생성 (Factory Method)"""
        obstacles = []
        
        # 비트마다 장애물 생성
        for beat_time in self._beats:
            obstacle = self._create_obstacle_at_beat(beat_time)
            obstacles.append(obstacle)
        
        # 주파수 변화에 따라 추가 장애물
        high_freq_obstacles = self._create_frequency_obstacles()
        obstacles.extend(high_freq_obstacles)
        
        return Course(obstacles)
    
    # Private 메서드
    def _create_obstacle_at_beat(self, time):
        """비트 위치에 장애물 생성"""
        # 해당 시간의 주파수 가져오기
        freq = self._get_frequency_at_time(time)
        
        # 주파수에 따라 높이 결정
        height = self._frequency_to_height(freq)
        
        return BeatObstacle(time, height)
    
    def _create_frequency_obstacles(self):
        """주파수 변화가 큰 지점에 장애물 생성"""
        obstacles = []
        # 구현 생략
        return obstacles
    
    def _get_frequency_at_time(self, time):
        """특정 시간의 주파수 값"""
        index = int(time * self._sample_rate / 512)  # hop_length
        if 0 <= index < len(self._spectral_centroids):
            return self._spectral_centroids[index]
        return 0
    
    def _frequency_to_height(self, freq):
        """주파수 → 장애물 높이 매핑"""
        # 0~5000Hz → 0~300px
        return min(int(freq / 5000 * 300), 300)
```

**OOP 원칙**:
- ✅ **Factory Pattern**: generate()로 Course 객체 생성
- ✅ **캡슐화**: 매핑 알고리즘 내부 숨김
- ✅ **단일 책임**: 코스 생성만

---

### 7.3 MusicProvider 추상 클래스 (Strategy Pattern)

```python
from abc import ABC, abstractmethod

class MusicProvider(ABC):
    """음악 플랫폼 추상 클래스 (Strategy Pattern)"""
    
    @abstractmethod
    def authenticate(self):
        """인증 (OAuth 등)"""
        pass
    
    @abstractmethod
    def get_playlists(self):
        """플레이리스트 목록 가져오기"""
        pass
    
    @abstractmethod
    def get_track(self, track_id):
        """트랙 정보 가져오기"""
        pass
    
    @abstractmethod
    def download_audio(self, track_id, output_path):
        """음원 다운로드 (또는 스트리밍 URL)"""
        pass

class SpotifyProvider(MusicProvider):
    """Spotify API 구현"""
    
    def __init__(self, client_id, client_secret):
        self._client_id = client_id
        self._client_secret = client_secret
        self._sp = None  # Spotipy 객체
    
    def authenticate(self):
        """Spotify OAuth 인증"""
        import spotipy
        from spotipy.oauth2 import SpotifyOAuth
        
        self._sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=self._client_id,
            client_secret=self._client_secret,
            redirect_uri="http://localhost:8888/callback",
            scope="user-library-read playlist-read-private"
        ))
    
    def get_playlists(self):
        """사용자 플레이리스트"""
        if not self._sp:
            self.authenticate()
        
        playlists = self._sp.current_user_playlists()
        return [
            {'id': p['id'], 'name': p['name']}
            for p in playlists['items']
        ]
    
    def get_track(self, track_id):
        """트랙 메타데이터"""
        track = self._sp.track(track_id)
        return {
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'preview_url': track['preview_url'],  # 30초 미리듣기
            'duration': track['duration_ms'] / 1000
        }
    
    def download_audio(self, track_id, output_path):
        """음원 다운로드 (제한적: 30초 미리듣기만)"""
        track = self.get_track(track_id)
        preview_url = track['preview_url']
        
        if not preview_url:
            raise ValueError("This track has no preview available")
        
        import requests
        audio_data = requests.get(preview_url).content
        
        with open(output_path, 'wb') as f:
            f.write(audio_data)

class LocalProvider(MusicProvider):
    """로컬 파일 구현"""
    
    def authenticate(self):
        """인증 불필요"""
        pass
    
    def get_playlists(self):
        """로컬 파일 목록"""
        import os
        music_dir = "user_music/"
        if not os.path.exists(music_dir):
            return []
        
        files = [f for f in os.listdir(music_dir) if f.endswith(('.mp3', '.wav'))]
        return [{'id': f, 'name': f} for f in files]
    
    def get_track(self, track_id):
        """파일 정보"""
        return {'name': track_id, 'path': f"user_music/{track_id}"}
    
    def download_audio(self, track_id, output_path):
        """이미 로컬에 있으므로 복사만"""
        import shutil
        source = f"user_music/{track_id}"
        shutil.copy(source, output_path)
```

**OOP 원칙**:
- ✅ **Strategy Pattern**: 플랫폼별 전략 교체 가능
- ✅ **다형성**: 모든 Provider 동일 인터페이스
- ✅ **개방-폐쇄**: 새 플랫폼 추가 쉬움

---

### 7.4 AutoPlayController 클래스 (Strategy)

```python
class AutoPlayController:
    """
    자동 플레이 로직 (Strategy Pattern)
    - 장애물 종류와 캐릭터 상태를 보고 자동 판단
    """
    
    def __init__(self, character):
        self._character = character
        self._last_action_time = 0
    
    def decide_action(self, obstacle, current_time):
        """
        장애물에 대한 자동 행동 결정
        :return: 'jump', 'duck', 'none'
        """
        # 쿨다운 체크 (너무 빠르게 연속 점프 방지)
        if current_time - self._last_action_time < 0.1:
            return 'none'
        
        if isinstance(obstacle, BeatObstacle):
            if obstacle.height > 100:
                self._last_action_time = current_time
                return 'jump'
            elif obstacle.height < 50:
                return 'none'  # 낮은 장애물은 그냥 통과
        
        elif isinstance(obstacle, FrequencyWall):
            self._last_action_time = current_time
            return 'jump'
        
        elif isinstance(obstacle, AmplitudeGap):
            self._last_action_time = current_time
            return 'duck'
        
        return 'none'
```

**OOP 원칙**:
- ✅ **Strategy Pattern**: 상황별 행동 전략
- ✅ **단일 책임**: 판단만 담당

---

### 7.5 클래스 다이어그램

```
AudioLoader
    - load(path)

AudioAnalyzer
    - analyze()
    ├─> _detect_beats()
    ├─> _extract_amplitude()
    └─> _extract_spectral_features()

CourseGenerator (Factory)
    - generate(audio_data)
    └─> Course

Course
    - obstacles[]
    - get_obstacles_at_time(t)

Obstacle (Abstract)
    ├── BeatObstacle
    ├── FrequencyWall
    └── AmplitudeGap

MusicProvider (Abstract)
    ├── SpotifyProvider
    ├── LocalProvider
    └── SunoProvider

Character
    - auto_jump()
    - auto_duck()

AutoPlayController (Strategy)
    - decide_action(obstacle)

Game (Main Controller)
    ├─> AudioAnalyzer
    ├─> CourseGenerator
    ├─> Course
    ├─> Character
    ├─> AutoPlayController
    ├─> ScoreManager
    └─> MusicProvider
```

---

## 8. 수익 실현 전략 (1인 개발자 로드맵)

### 📅 타임라인

#### Phase 1: MVP 출시 (1~3개월)
**목표**: 무료 버전 출시 → 사용자 확보

**액션**:
1. GitHub에 오픈소스로 공개
2. Reddit (r/Python, r/gamedev, r/indiedev) 홍보
3. YouTube 시연 영상 제작
4. Product Hunt 등록

**예상 결과**:
- 초기 50~200 다운로드 (오픈소스 커뮤니티)
- 첫 수익: $0~10/월 (1~2명 얼리어답터 구독)

---

#### Phase 2: 프리미엄 기능 추가 (4~6개월)
**목표**: 첫 구독자 확보 → 제품 검증

**액션**:
1. 프리미엄 기능 개발 (Spotify 연동, 광고 제거)
2. 가격 실험 ($1.99, $2.99, $4.99)
3. 무료 체험 7일 제공
4. Discord 커뮤니티 구축

**예상 결과**:
- 300~500 MAU (Monthly Active Users)
- 전환율 0.5~1% → 2~5명 구독
- 총 수익: $30~60/월 (구독 + 스킨)

---

#### Phase 3: 음악 플랫폼 파트너십 (7~12개월)
**목표**: Spotify/벅스 제휴 → 수익 다각화

**액션**:
1. **Spotify Developer Program 신청**
   - 10,000+ 월간 스트리밍 달성
   - "Spotify로 플레이" 기능 강조
   - Spotify 비즈니스 개발팀 컨택

2. **벅스/멜론 컨택**
   - 한국 시장 통계 준비 (MAU, 재생 시간)
   - 파일럿 프로그램 제안
   - "벅스에서 듣기" 버튼 통합

3. **Suno 교차 프로모션**
   - Suno Reddit/Discord에 홍보
   - Suno 팀에 이메일 (partnerships@)
   - 상호 사용자 유입 구조

**예상 결과**:
- 1,000~1,500 MAU
- Spotify 연동으로 전환율 향상 → 10~20명 구독
- 총 수익: $80~120/월

---

#### Phase 4: 확장 및 성장 (13개월~)
**목표**: 모바일 진출 → 대규모 수익

**액션**:
1. **모바일 앱 개발** (React Native 또는 Flutter)
   - iOS App Store
   - Google Play Store
2. **인플루언서 마케팅**
   - 유튜브 게임 리뷰어 컨택
   - TikTok 바이럴 콘텐츠 제작
3. **기업 라이센싱**
   - 음악 교육 기관에 판매
   - 피트니스 앱과 협업

**예상 결과**:
- 2,000~3,000 다운로드 (누적)
- 모바일 앱 개발 시작 (React Native/Flutter)
- 수익: $150~250/월 (PC 버전 안정화)

---

### 💡 빠른 수익화 팁 (자본 없이)

#### 1. 오픈소스 + 프리미엄 모델
- GitHub Star 10개 → Hacker News 게시판에 홍보
- "Made with ❤️ by solo dev" 스토리텔링
- Buy Me a Coffee 버튼 추가 (후원 유도)

#### 2. 콘텐츠 마케팅 (무료)
- **Dev.to / Medium 블로그 포스트**:
  - "How I Built a Music Visualizer Game with Python"
  - "Using Librosa to Turn Songs into Game Levels"
  - "1인 개발자의 첫 수익 $100 달성기"
- **YouTube 개발 일지**:
  - "Music Sprint Devlog #1: Audio Analysis"
  - 구독자 1,000명 달성 → 광고 수익

#### 3. 커뮤니티 활용
- r/Python, r/gamedev, r/indiegames에 주 1회 업데이트
- Discord 서버 개설 (무료)
- "주간 챌린지" 이벤트 (특정 곡으로 경쟁)

#### 4. 초기 사용자 인센티브
- 첫 100명 베타 테스터 → 평생 프리미엄 무료
- 친구 추천 시 1개월 무료 (바이럴 효과)

---

## 9. 리스크 관리

### 기술적 리스크

| 리스크 | 확률 | 영향 | 대응책 |
|--------|------|------|--------|
| 음원 분석 성능 저하 | 중 | 높음 | 오디오 길이 제한 (5분), 다운샘플링 |
| Spotify API 제한 | 중 | 중 | 30초 미리듣기만 사용, Rate Limit 준수 |
| 광고 SDK 통합 실패 | 낮 | 중 | 웹뷰 대안 사용 또는 초기 광고 생략 |
| 저작권 문제 | 낮 | 높음 | 사용자 업로드 책임, DMCA 정책 명시 |

### 비즈니스 리스크

| 리스크 | 확률 | 영향 | 대응책 |
|--------|------|------|--------|
| 사용자 유입 부족 | 높음 | 높음 | 무료 오픈소스 → 커뮤니티 활용, Reddit 마케팅 |
| 전환율 저조 (<0.5%) | 중 | 중 | 가격 실험, 무료 체험 연장, 프리미엄 기능 강화 |
| Spotify/벅스 공식 파트너십 실패 | 매우 높음 | 낮음 | 예상됨 - 간접 효과만 기대, 직접 수익 의존 안 함 |
| 경쟁 게임 출현 | 낮 | 중 | 독창성 유지, 빠른 업데이트, 커뮤니티 강화 |
| 초기 수익 부족 ($50/월 미만) | 중 | 중 | 장기적 관점 유지, 포트폴리오 가치 우선 |

---

## 10. 법적 고려사항

### 저작권 (음원)
**문제**: 사용자가 업로드한 음원의 저작권

**대응**:
- ✅ **면책 조항**: "사용자가 업로드한 음원의 저작권 책임은 사용자에게 있음"
- ✅ **DMCA 정책**: 저작권자 신고 시 즉시 삭제
- ✅ **라이선스 안내**: "본인 소유 또는 라이선스가 있는 음원만 업로드하세요"
- ✅ **Spotify 연동 시**: Spotify API 약관 준수 (30초 preview만 사용)

### 음악 플랫폼 API 약관
- **Spotify**: 상업적 사용 허용, 하지만 전체 곡 다운로드 금지 → 30초 preview만
- **벅스/멜론**: API 제공 여부 확인 필요 → 없으면 제휴 제안

### 개인정보 보호
- 최소 정보 수집 (이메일만)
- GDPR/CCPA 준수 (유럽/미국 사용자 시)

---

## 11. 성공 지표 (KPI)

### 제품 지표
- **DAU** (Daily Active Users): 20~50명 (1개월), 100~200명 (6개월), 300~500명 (1년)
- **재방문율**: 20% 이상 (초기 목표)
- **평균 플레이 시간**: 10분/세션
- **곡당 재플레이율**: 15% (같은 곡을 다시 플레이)

### 수익 지표
- **프리미엄 전환율**: 0.5~1% (초기), 1~2% (6개월 후)
- **월 구독 수익**: $10~30 (3개월), $50~80 (6개월), $100~150 (1년)
- **스킨 판매 수익**: $10~20 (3개월), $30~50 (6개월), $50~80 (1년)
- **총 월 수익**: $20~50 (3개월), $80~130 (6개월), $150~230 (1년)

### 커뮤니티 지표
- **GitHub Stars**: 20~50 (3개월), 100~200 (6개월), 300~500 (1년)
- **Discord 멤버**: 10~20 (3개월), 30~50 (6개월), 80~150 (1년)
- **소셜 공유**: 월 10~20회 이상

---

## 12. 결론

### 핵심 포인트
1. ✅ **기술적 독창성**: 음원 파형 기반 자동 코스 생성 (Librosa + PyGame)
2. ✅ **시장 차별화**: 방치형 + 음악 + 소셜 = 기존에 없던 조합
3. ✅ **수익 가능성**: Freemium + 광고 + 제휴 = 다각화된 수익 모델
4. ✅ **1인 개발 최적화**: 오픈소스 + 커뮤니티 마케팅 = 자본 불필요
5. ✅ **확장성**: PC → 모바일 → 웹 → VR

### 첫 3개월 목표
- [ ] MVP 개발 완료 (Phase 1~4)
- [ ] GitHub 공개 및 20~50 Stars
- [ ] 첫 수익 $20~50 달성
- [ ] Spotify 연동 완료
- [ ] 첫 유료 구독자 3~5명 확보

### 1년 목표
- [ ] 300~500 DAU 달성
- [ ] 월 수익 $150~230 달성
- [ ] GitHub 300~500 Stars
- [ ] 모바일 앱 개발 시작 (React Native/Flutter)
- [ ] 커뮤니티 80~150명 구축

### 장기 목표 (2년차)
- [ ] 모바일 앱 출시 (iOS/Android)
- [ ] AdMob 광고 통합 → 수익 2~3배 증가
- [ ] 월 수익 $400~800 달성
- [ ] 5,000+ 누적 다운로드

---

**Music Sprint는 단순한 게임이 아닌, 음악을 새롭게 경험하는 플랫폼입니다.**

**1인 개발자로서 기술력과 비즈니스 감각을 동시에 증명할 수 있는 프로젝트입니다!** 🎵🏃‍♂️💰
