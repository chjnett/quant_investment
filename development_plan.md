# 개발 계획 및 로드맵: Alpha Sentinel OS

본 문서는 [PRD](prd.md)를 기반으로 작성된 개발 계획입니다.

## 1. 프로젝트 목표
장기 퀀트 투자를 위한 AI 에이전트 시스템 구축. 거시 경제 및 정성적 데이터를 통합하여 최적의 포트폴리오 제안 및 관리.

---

## 2. 상세 개발 태스크

### Phase 0: 환경 설정 (Environment Setup)
- [x] 프로젝트 디렉토리 구조 생성
- [x] Git 저장소 초기화
- [ ] **Docker 환경 구성**
  - [ ] Frontend (Next.js) Dockerfile
  - [ ] Backend (Python) Dockerfile
  - [ ] docker-compose.yml (PostgreSQL 포함)
- [ ] 환경 변수 설정 (.env)

### Phase 1: 인프라 및 데이터 수집 (Infrastructure & Data Collection)
- **Database**
  - [ ] Neon PostgreSQL 연동 (또는 로컬 Docker Postgres)
  - [ ] DB 스키마 정의 (`init_db.sql`)
    - `company_info`, `macro_indicators`, `financial_records`, `investment_thesis`
  - [ ] DB 연결 모듈 구현 (`api/core/database.py`)
- **Data Collectors**
  - [ ] FRED API 연동 (`api/collectors/fred.py`) - 거시 지표 수집
  - [ ] yfinance 연동 (`api/collectors/market.py`) - 주가 데이터 수집
  - [ ] 데이터 수집 스케줄러 설정 (Cron Jobs)

### Phase 2: 핵심 로직 구현 (Core Logic & Agents)
- **Calculators (Deterministic Layer)**
  - [ ] 재무 지표 계산기 (`api/calculators/finance.py`) - PER, RBR, GPA 등
  - [ ] 거시 지표 정규화 로직 (`api/calculators/macro.py`)
- **Agents (Reasoning Layer)**
  - [ ] LangGraph 기본 설정
  - [ ] **Macro Sentry**: Risk-On/Off 판별 로직 (`api/agents/macro.py`)
  - [ ] **Sector Strategist**: 섹터/ETF 분석 로직 (`api/agents/strategist.py`)
  - [ ] **CIO Agent**: 포트폴리오 비중 결정 로직 (`api/agents/cio.py`)
- **Integration**
  - [ ] 에이전트 간 상태 공유 로직 (`api/core/state.py`)

### Phase 3: NLP 및 고급 분석 (NLP & Insight)
- **Data Collectors**
  - [ ] Open DART API 연동 (`api/collectors/dart.py`) - 공시 데이터
- **Agents**
  - [ ] **Insight Analyst**: MD&A 텍스트 분석 및 감성 분석 (`api/agents/insight.py`)
- **Hypothesis Tracker**
  - [ ] 투자 가설 생성 및 저장 로직
  - [ ] 가설 감사(Audit) 시스템 구현

### Phase 4: UI/UX 개발 (Frontend)
- **Components**
  - [ ] Design System 구축 (Tailwind CSS, Shadcn UI)
  - [ ] `MarketCard` 컴포넌트 (`app/components/market-card.tsx`)
  - [ ] `AgentLogViewer` 컴포넌트 (`app/components/agent-logs.tsx`)
- **Pages**
  - [ ] 대시보드 메인 (`app/(dashboard)/page.tsx`) - 투자 현황 시각화
  - [ ] 투자 가설 관리 페이지 (`app/thesis/page.tsx`)
- **Integration**
  - [ ] Backend API 연동 (`app/services/`)

### Phase 5: 테스트 및 최적화 (Test & Optimize)
- [ ] 전체 시스템 통합 테스트
- [ ] Vercel 배포 및 운영 환경 테스트
- [ ] 비용 최적화 점검 (API 호출 최소화, 캐싱 적용)

---

## 3. 우선순위
1. 도커 환경 구성을 통한 로컬 개발 환경 안정화
2. DB 스키마 적용 및 기본 데이터 수집(FRED, yfinance)
3. 핵심 에이전트(Macro, Sector) 구현
4. 프론트엔드 대시보드 연동
