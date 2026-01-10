import pandas as pd
import numpy as np
from sqlalchemy import text
import sys
import os

# 공통 모듈 임포트
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from api.db_utils import get_db_engine

def load_price_data(engine, ticker_id, limit=365):
    """DB에서 특정 종목의 과거 데이터를 가져옴 (최신순 -> 날짜 오름차순 정렬)"""
    query = text("""
        SELECT date, open, high, low, close, volume
        FROM market_data
        WHERE ticker_id = :ticker_id
        ORDER BY date DESC
        LIMIT :limit
    """)
    
    with engine.connect() as conn:
        df = pd.read_sql(query, conn, params={"ticker_id": ticker_id, "limit": limit})
    
    if df.empty:
        return None
    
    # 시간 순서대로 정렬 (과거 -> 현재)해야 지표 계산 가능
    df = df.sort_values(by="date").reset_index(drop=True)
    return df

def calculate_indicators(df):
    """기술적 지표 계산 (SMA, RSI, Bollinger Bands)"""
    # 1. 이동평균선 (SMA)
    df['SMA_20'] = df['close'].rolling(window=20).mean()
    df['SMA_60'] = df['close'].rolling(window=60).mean()
    
    # 2. RSI (Relative Strength Index) - 14일 기준
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    
    rs = gain / loss
    df['RSI_14'] = 100 - (100 / (1 + rs))
    
    # 3. 볼린저 밴드 (20일, 2표준편차)
    df['BB_Middle'] = df['SMA_20']
    df['BB_Std'] = df['close'].rolling(window=20).std()
    df['BB_Upper'] = df['BB_Middle'] + (df['BB_Std'] * 2)
    df['BB_Lower'] = df['BB_Middle'] - (df['BB_Std'] * 2)
    
    return df

def get_latest_analysis(symbol):
    """특정 종목의 가장 최근 분석 결과 반환 (AI에게 넘겨줄 데이터)"""
    engine = get_db_engine()
    if not engine: return None

    # 1. 종목 ID 찾기
    with engine.connect() as conn:
        result = conn.execute(text("SELECT id FROM tickers WHERE symbol = :symbol"), {"symbol": symbol})
        row = result.fetchone()
        if not row:
            print(f"❌ Symbol not found: {symbol}")
            return None
        ticker_id = row[0]

    # 2. 데이터 로드
    df = load_price_data(engine, ticker_id)
    if df is None or len(df) < 60:
        print(f"⚠️ Not enough data for analysis: {symbol}")
        return None

    # 3. 지표 계산
    df = calculate_indicators(df)
    
    # 4. 가장 최근 데이터(마지막 행) 추출
    latest = df.iloc[-1]
    
    # 5. 분석 요약 리턴
    analysis = {
        "symbol": symbol,
        "date": str(latest['date']),
        "price": latest['close'],
        "indicators": {
            "RSI_14": round(latest['RSI_14'], 2) if not pd.isna(latest['RSI_14']) else -1,
            "SMA_20": round(latest['SMA_20'], 2) if not pd.isna(latest['SMA_20']) else -1,
            "BB_Position": "Inside" # 기본값
        }
    }
    
    # 볼린저 밴드 위치 판단
    if latest['close'] > latest['BB_Upper']:
        analysis['indicators']['BB_Position'] = "Overbought (Above Upper Band)"
    elif latest['close'] < latest['BB_Lower']:
        analysis['indicators']['BB_Position'] = "Oversold (Below Lower Band)"
        
    return analysis

if __name__ == "__main__":
    # 테스트 실행
    print("--- [Analyzer Test] ---")
    test_symbol = "AAPL"
    result = get_latest_analysis(test_symbol)
    if result:
        print(f"✅ Analysis Result for {test_symbol}:")
        print(result)
    else:
        print("❌ Analysis Failed")
