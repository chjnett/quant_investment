```sql
-- tickers 테이블: 주식 종목 정보를 저장하는 테이블
CREATE TABLE IF NOT EXISTS tickers (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10) UNIQUE NOT NULL,
    name VARCHAR(255),
    sector VARCHAR(100)
);
-- id: 고유 자동증가 번호 (1, 2, 3...)
-- symbol: 종목코드 (예: 'AAPL') - 중복 불가, 필수 입력
-- name: 종목명 (예: 'Apple Inc.')
-- sector: 종목분류/섹터 (예: 'Technology')


-- agent_logs 테이블: AI 에이전트 및 시스템 로그를 기록하는 테이블
CREATE TABLE IF NOT EXISTS agent_logs (
    id SERIAL PRIMARY KEY,
    agent_name VARCHAR(50),
    log_level VARCHAR(20),
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- id: 고유 자동증가 번호
-- agent_name: 로그를 남긴 주체/에이전트 이름
-- log_level: 로그 레벨 (INFO, ERROR, WARNING 등)
-- message: 상세 로그 메시지 (길이 제한 없는 텍스트)
-- created_at: 로그 생성 시간 (입력 안 하면 현재 시간 자동 기록)
```
