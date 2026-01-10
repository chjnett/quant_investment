-- macro_economic 테이블: 거시경제 지표 저장
CREATE TABLE IF NOT EXISTS macro_economic (
    id SERIAL PRIMARY KEY,
    indicator_name VARCHAR(50) NOT NULL, -- 예: 'GDP', 'FEDFUNDS', 'UNRATE'
    date DATE NOT NULL,
    value NUMERIC,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(indicator_name, date)
);
-- indicator_name: FRED Series ID (예: FEDFUNDS = 미국 금리)
-- value: 지표 값
