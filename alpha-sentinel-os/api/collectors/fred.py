from fredapi import Fred
import pandas as pd
from sqlalchemy import text
import sys
import os
from datetime import datetime
from dotenv import load_dotenv

# 공통 모듈 임포트
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from api.db_utils import get_db_engine

# .env 파일 명시적 로드
load_dotenv()

# FRED API KEY (환경변수 필수)
FRED_KEY = os.getenv("FRED_API_KEY")

# 수집할 주요 경제 지표 목록 (Series ID)
INDICATORS = {
    "FEDFUNDS": "Interest Rate (Federal Fans)",   # 금리
    "GDP": "Gross Domestic Product",              # GDP
    "UNRATE": "Unemployment Rate",                # 실업률
    "CPIAUCSL": "CPI (Consumer Price Index)",     # 소비자 물가 지수
    "DGS10": "10-Year Treasury Yield"             # 10년물 국채 금리
}

def save_fred_data(engine, series_id, df):
    data = []
    # fredapi가 리턴하는건 pandas Series 형태일 수 있음
    # Index: date, Value: 값
    
    # Series -> DataFrame 변환
    if isinstance(df, pd.Series):
        df = df.to_frame(name='value')
        
    for date, row in df.iterrows():
        val = row['value']
        # NaN 체크 (데이터 없는 날짜 건너뛰기)
        if pd.isna(val): continue
        
        data.append({
            "indicator": series_id,
            "date": date.date(),
            "value": float(val)
        })
        
    if not data: return

    with engine.connect() as conn:
        stmt = text("""
            INSERT INTO macro_economic (indicator_name, date, value)
            VALUES (:indicator, :date, :value)
            ON CONFLICT (indicator_name, date) DO UPDATE
            SET value = EXCLUDED.value, created_at = CURRENT_TIMESTAMP;
        """)
        conn.execute(stmt, data)
        conn.commit()
    print(f"Saved {len(data)} records for {series_id}")

def run():
    print("=== [FRED Macro Data Collector] Start ===")
    
    if not FRED_KEY:
        print(" Error: FRED_API_KEY not found in env.")
        return

    engine = get_db_engine()
    if not engine: return
    
    try:
        fred = Fred(api_key=FRED_KEY)
        
        for series_id, name in INDICATORS.items():
            print(f"Fetching {name} ({series_id})...")
            try:
                # 최근 5년치 데이터 수집
                df = fred.get_series(series_id, observation_start='2020-01-01')
                save_fred_data(engine, series_id, df)
            except Exception as e:
                print(f"   Failed to fetch {series_id}: {e}")
                
    except Exception as e:
        print(f" FRED init failed: {e}")

    print("=== [FRED Macro Data Collector] End ===")

if __name__ == "__main__":
    run()
