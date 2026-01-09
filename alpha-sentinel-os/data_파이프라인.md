# 데이터 파이프라인 설계 및 체크리스트

이 문서는 현재 구축된 인프라를 점검하고, 향후 퀀트 투자 시스템(`Alpha Sentinel OS`)을 위한 데이터 파이프라인 설계 가이드를 제공합니다.

---

## ✅ 1. 현재 구축 상태 체크리스트 (Current Status Checklist)

지금까지 완료한 작업들을 점검합니다. 모두 체크가 되어야 다음 단계로 넘어갈 준비가 완료된 것입니다.

### 인프라 (Infrastructure)
- [x] **Docker 환경 구성**: `docker-compose.yml`을 통해 Frontend, Backend, DB 컨테이너 구성 완료.
- [x] **Database 실행**: PostgreSQL 컨테이너(`alpha-sentinel-db`) 정상 실행 확인.
- [x] **데이터 영속성 확보**: Docker Volume(`postgres_data`)을 통한 DB 데이터 보존 설정 완료.
- [x] **외부 접속 환경**: DBeaver 등 외부 툴 접속을 위한 포트 설정(`5435`) 및 연결 성공.

### 데이터베이스 스키마 (Schema)
- [x] **기본 테이블 생성**:
  - `tickers`: 주식 종목 마스터 데이터 (Symbol, Name, Sector).
  - `agent_logs`: 시스템 및 AI 에이전트 활동 로그.
- [x] **무결성 제약조건 설정**: Primary Key(Serial), Unique(Symbol), Not Null 등 기본 제약조건 적용.
- [x] **초기화 스크립트 연동**: `init_db.sql`이 컨테이너 시작 시 자동 실행되도록 마운트 설정.

---

## 🚀 2. 데이터 파이프라인 설계 (Data Pipeline Design)

퀀트 시스템의 핵심은 **"데이터 수집 -> 저장 -> 가공 -> 분석"**의 흐름을 자동화하는 것입니다.

### 🏗️ 전체 아키텍처 개요
```mermaid
graph LR
    A[Data Sources] -->|수집 (Collector)| B(Backend API / Scheduler)
    B -->|Raw Data 저장| C[(PostgreSQL DB)]
    C -->|데이터 로드| D{AI Agent / Analysis}
    D -->|결과/로그 저장| C
    B -->|데이터 제공| E[Frontend (Next.js)]
```

### 💧 단계별 설계 가이드

#### Phase 1. 데이터 수집 (Ingestion)
외부 금융 API로부터 데이터를 가져오는 단계입니다.
- **대상 데이터**: 주가(OHLCV), 기업 재무 정보, 뉴스 등.
- **구현 방법**:
  - `Backend Container` 내부에 **Scheduler**(APScheduler 또는 Celery) 구축.
  - 정해진 시간(예: 장 마감 후)에 외부 API 호출.
- **필요 라이브러리**: `yfinance`, `ccxt`, `requests` 등.

#### Phase 2. 데이터 저장 (Storage)
수집된 데이터를 PostgreSQL에 적재합니다.
- **종목 정보 (`tickers`)**: 수집 대상 종목 리스트 관리. (현재 생성됨)
- **시계열 데이터 (`market_data`)**: **[추가 생성 필요]**
  - 주가 데이터는 시간에 따라 계속 쌓이므로 별도 테이블이 필요합니다.
  - 구조 예시: `timestamp`, `ticker_id`, `open`, `high`, `low`, `close`, `volume`.
- **에이전트 로그 (`agent_logs`)**: 수집 성공/실패 여부를 기록하여 모니터링. (현재 생성됨)

#### Phase 3. 데이터 가공 및 분석 (Processing)
저장된 데이터를 기반으로 지표를 계산하거나 AI가 판단을 내립니다.
- **전처리**: 결측치(Missing Value) 제거, 수정주가 반영.
- **기술적 지표 계산**: 이동평균선(MA), RSI, Bollinger Bands 등 계산 후 DB 업데이트 또는 메모리 처리.
- **AI 판단**: LLM 또는 알고리즘이 가공된 데이터를 읽고 매수/매도 시그널 생성.

#### Phase 4. 데이터 서빙 (Serving)
최종 사용자(Web)에게 데이터를 보여줍니다.
- **API 개발**: Frontend가 DB 데이터를 요청할 수 있는 REST API 엔드포인트 생성.
- **시각화**: Next.js에서 차트 라이브러리를 사용해 주가 및 AI 매매 시점 시각화.

---

## 📅 3. 다음 실행 단계 (Next Steps)

1. **시계열 데이터 테이블 생성 (`market_data`)**
   - 주가 데이터를 담을 그릇을 만들어야 합니다 (현재 가장 시급함).
2. **데이터 수집 스크립트 작성 (Python)**
   - `yfinance` 등을 이용해 `tickers` 테이블에 있는 종목들의 과거 1년 치 주가를 긁어오는 파이썬 함수 작성.
3. **API 엔드포인트 연결**
   - 수집된 데이터를 Frontend에서 조회할 수 있도록 `/api/prices` 와 같은 백엔드 라우터 구현.
