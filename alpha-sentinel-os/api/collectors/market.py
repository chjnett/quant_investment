import yfinance as yf
import pandas as pd
from sqlalchemy import text
import time
import sys
import os

# 상위 폴더(api)의 모듈을 임포트하기 위한 경로 설정
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from api.db_utils import get_db_engine

def get_tickers(engine):
    """DB에서 수집 대상 종목 가져오기"""
    with engine.connect() as conn:
        result = conn.execute(text("SELECT id, symbol FROM tickers"))
        return result.fetchall()

def fetch_market_data(symbol, period="1y"):
    """yfinance 주가 수집"""
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=period)
        if df.empty:
            return None
        return df
    except Exception as e:
        print(f"⚠️ {symbol} yfinance 에러: {e}")
        return None

def save_to_db(engine, ticker_id, df):
    """데이터 저장 (중복 시 업데이트)"""
    data = []
    for date, row in df.iterrows():
        data.append({
            "ticker_id": ticker_id,
            "date": date.date(),
            "open": float(row['Open']),
            "high": float(row['High']),
            "low": float(row['Low']),
            "close": float(row['Close']),
            "volume": int(row['Volume'])
        })
    
    if not data:
        return

    with engine.connect() as conn:
        stmt = text("""
            INSERT INTO market_data (ticker_id, date, open, high, low, close, volume)
            VALUES (:ticker_id, :date, :open, :high, :low, :close, :volume)
            ON CONFLICT (ticker_id, date) DO UPDATE 
            SET close = EXCLUDED.close, volume = EXCLUDED.volume,
                high = EXCLUDED.high, low = EXCLUDED.low, open = EXCLUDED.open,
                created_at = CURRENT_TIMESTAMP;
        """)
        conn.execute(stmt, data)
        conn.commit()
    print(f"   Success: {len(data)} rows saved.")

def run():
    print("=== [Market Data Collector] Start ===")
    engine = get_db_engine()
    if not engine: return

    tickers = get_tickers(engine)
    print(f"Target Tickers: {len(tickers)}")

    for t_id, symbol in tickers:
        print(f"Fetching {symbol}...")
        df = fetch_market_data(symbol)
        if df is not None:
            save_to_db(engine, t_id, df)
        else:
            print("   No Data found.")
        time.sleep(1)
    
    print("=== [Market Data Collector] End ===")
    
if __name__ == "__main__":
    run()
