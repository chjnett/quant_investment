# [PRD] AI 에이전트 기반 장기 퀀트 투자 시스템: Alpha Sentinel OS
## 1. 프로젝트 개요 (Project Overview)
* **제품명**: Alpha Sentinel OS
* **목표**: 2~3년 단위의 장기 투자를 위해 거시 경제 지표부터 기업의 정성적 공시 데이터까지 통합 분석하여, 감정을 배제한 최적의 포트폴리오를 제안하고 관리하는 AI 에이전트 시스템 구축.
* **대상 유저**: 데이터 기반의 가치 투자를 지향하며, 인프라 비용 부담 없이 클라우드 환경에서 자동화 시스템을 운영하고자 하는 개인 투자자.
## 2. 핵심 투자 철학 (Core Philosophy)
1. **Top-Down Priority**: 거시 경제가 무너진 시장(Crisis)에서는 개별 종목의 우량함보다 '생존'과 '현금화'가 우선이다.
2. **Hybrid Alpha**: 전통적 퀀트의 수치 데이터(PBR, ROE 등)에 LLM의 비정형 데이터(공시 뉘앙스, 뉴스 감성) 해석력을 더해 초과 수익을 창출한다.
3. **Thesis-Driven Exit**: 매수 가격이 아닌, 매수 당시 설정한 '투자 가설'이 깨졌을 때 기계적으로 매도한다.
## 3. 기능 요구사항 (Functional Requirements)
### 3.1. 멀티 에이전트 추론 체인 (LangGraph)
* **Macro Sentry**: FRED/yfinance 데이터를 분석하여 투자 가능 여부(Risk-On/Off) 판정 및 글로벌 킬스위치 가동.
* **Sector Strategist**: 현재 거시 환경에 가장 유리한 업종(Sector) 및 ETF 모멘텀 분석.
* **Fundamental Engine (Pandas)**: AI 개입 없이 코드로만 GPA, PBR, 부채비율 등 수치 지표 계산 및 후보군 스크리닝.
* **Insight Analyst (NLP)**: 후보 종목의 사업보고서 내 'MD&A' 섹션을 분석하여 경영진의 자신감 및 잠재 리스크 수치화.
* **CIO Agent**: 모든 데이터를 종합하여 최종 포트폴리오 비중을 결정하고 투자 가설 리포트 생성.
### 3.2. 데이터 파이프라인 및 비동기 처리
* **Atomic Task Chaining**: Vercel의 60초 타임아웃을 극복하기 위해 분석 단계를 독립된 함수로 분리하고 DB를 통해 상태를 전이함.
* **Idempotency Logic**: 네트워크 오류로 중단 시 마지막 성공 지점부터 재개하는 멱등성 보장.
* **Data Scraper**: 월간(거시), 분기(재무), 주간(시세) 단위의 스케줄링 수집.
### 3.3. 투자 가설 관리 (Hypothesis Tracker)
* **Snapshot**: 매수 시점의 재무 수치와 AI가 분석한 정성적 이유를 JSONB 형식으로 기록.
* **Quarterly Audit**: 실적 발표마다 AI가 가설 준수 여부를 자동 체크하여 '가설 유지/매도' 의견 제시.
## 4. 기술 아키텍처 (Technical Architecture)
* **Frontend**: Next.js (App Router), Tailwind CSS (Shadcn UI).
* **Backend**: Vercel Python Runtime (Serverless Functions), LangGraph.
* **Database**: **Neon PostgreSQL (Region: Asia Pacific - Singapore)**.
* **AI Model**: GPT-4o-mini (Preprocessing), Claude 3.5 Sonnet (Reasoning).
* **Infrastructure**: Vercel Cron Jobs (Scheduling), GitHub Actions (CI/CD).

## 5. 데이터 스키마 설계 (Data Schema)

* `company_info`: 기업 메타데이터 및 분석 활성화 상태.
* `macro_indicators`: 금리, CPI, VIX 등 거시 지표 시계열 데이터.
* `financial_records`: Pandas 엔진이 가공한 확정적 재무 지표.
* `investment_thesis`: 매수 가설, 매도 트리거(JSON), 감사 로그(Audit Log).

## 6. 비기능적 요구사항 (Non-Functional Requirements)

* **비용 관리**: 모든 파이프라인은 무료 티어(Vercel Hobby, Neon Free) 내에서 구동되도록 설계.
* **정합성**: AI의 수치 환각을 방지하기 위해 결정론적 계산 레이어(Pandas)를 AI 추론 레이어와 엄격히 분리.
* **보안**: 모든 API Key는 Vercel Secret 환경 변수로 관리.

## 7. 단계별 로드맵 (Execution Roadmap)

1. **Phase 1 (Infra)**: Neon DB 구축 및 FRED/yfinance 기반 거시 데이터 자동 수집기 완성.
2. **Phase 2 (Logic)**: LangGraph 기반 추론 워크플로우 및 Vercel 비동기 체이닝 구현.
3. **Phase 3 (NLP)**: Open DART 연동 및 공시 감성 분석/투자 가설 트래커 구축.
4. **Phase 4 (UI)**: Next.js 대시보드 연결 및 전체 시스템 자동 가동 테스트.

---




#시스템 아키텍처
/alpha-sentinel-os
├── /api                    # [Backend] Vercel Python Serverless Functions
│   ├── /agents             # LangGraph 기반 에이전트 로직
│   │   ├── macro.py        # Macro Sentry 에이전트
│   │   ├── strategist.py   # Sector Strategist 에이전트
│   │   ├── insight.py      # NLP Insight Analyst 에이전트
│   │   └── cio.py          # 최종 의사결정 CIO 에이전트
│   ├── /calculators        # 결정론적 계산 레이어 (Pandas)
│   │   ├── finance.py      # 재무 지표 계산기 (PER, ROE, GPA 등)
│   │   └── macro.py        # 거시 경제 지표 정규화 로직
│   ├── /collectors         # 외부 데이터 수집기 (ETL)
│   │   ├── dart.py         # Open DART API 연동
│   │   ├── fred.py         # FRED API 연동
│   │   └── market.py       # yfinance 연동
│   ├── /core               # 공통 코어 모듈
│   │   ├── database.py     # Neon DB 연결 및 세션 관리
│   │   ├── security.py     # API 보안 및 키 관리
│   │   └── state.py        # 에이전트 상태(State) 관리 로직
│   └── index.py            # Vercel API 엔트리 포인트 (FastAPI/Flask)
│
├── /app                    # [Frontend] Next.js (App Router)
│   ├── /(dashboard)        # 대시보드 관련 페이지 그룹
│   │   ├── page.tsx        # 메인 투자 현황판
│   │   └── layout.tsx
│   ├── /thesis             # 투자 가설 관리 페이지
│   ├── /components         # 공통 UI 컴포넌트 (Shadcn UI)
│   │   ├── agent-logs.tsx  # 에이전트 사고 로그 뷰어
│   │   └── market-card.tsx # 시장 지표 카드
│   ├── /lib                # 프론트엔드 유틸리티 (Supabase/Neon 클라이언트)
│   └── /services           # 백엔드 API 호출 로직
│
├── /scripts                # DB 마이그레이션 및 초기화 스크립트
│   ├── init_db.sql         # Neon DB 스키마 SQL
│   └── seed_data.py        # 초기 종목(Ticker) 데이터 주입
│
├── vercel.json             # Vercel Cron 및 Routing 설정 파일
├── requirements.txt        # Python 종속성 (pandas, langgraph, psycopg2 등)
├── package.json            # Node.js 종속성 (next, tailwind, lucide-react 등)
├── .env.example            # 환경 변수 템플릿
└── README.md               # 프로젝트 문서