from sqlalchemy import text
import sys
import os

# 공통 모듈 임포트
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from api.db_utils import get_db_engine

# S&P 500 11개 주요 섹터 ETF + 나스닥/S&P 지수
SECTOR_ETFS = [
    # 시장 지수
    {"symbol": "SPY", "name": "SPDR S&P 500 ETF Trust", "sector": "Market"},
    {"symbol": "QQQ", "name": "Invesco QQQ Trust", "sector": "Market"},
    
    # 11개 주요 섹터
    {"symbol": "XLK", "name": "Technology Select Sector SPDR", "sector": "Technology"},
    {"symbol": "XLV", "name": "Health Care Select Sector SPDR", "sector": "Healthcare"},
    {"symbol": "XLF", "name": "Financial Select Sector SPDR", "sector": "Financial"},
    {"symbol": "XLY", "name": "Consumer Discretionary Select Sector", "sector": "Consumer Discretionary"},
    {"symbol": "XLP", "name": "Consumer Staples Select Sector SPDR", "sector": "Consumer Staples"},
    {"symbol": "XLE", "name": "Energy Select Sector SPDR", "sector": "Energy"},
    {"symbol": "XLI", "name": "Industrial Select Sector SPDR", "sector": "Industrial"},
    {"symbol": "XLB", "name": "Materials Select Sector SPDR", "sector": "Materials"},
    {"symbol": "XLU", "name": "Utilities Select Sector SPDR", "sector": "Utilities"},
    {"symbol": "XLRE", "name": "Real Estate Select Sector SPDR", "sector": "Real Estate"},
    {"symbol": "XLC", "name": "Communication Services Select Sector", "sector": "Communication Services"},
    
    # + 안전자산/채권 (Macro Sentry 보조용)
    {"symbol": "TLT", "name": "iShares 20+ Year Treasury Bond ETF", "sector": "Bond"},
    {"symbol": "GLD", "name": "SPDR Gold Shares", "sector": "Commodity"}
]

def seed_tickers():
    print("--- Seeding Sector ETFs ---")
    engine = get_db_engine()
    if not engine: return

    with engine.connect() as conn:
        for etf in SECTOR_ETFS:
            try:
                # 이미 있으면 무시하고 진행
                stmt = text("""
                    INSERT INTO tickers (symbol, name, sector)
                    VALUES (:symbol, :name, :sector)
                    ON CONFLICT (symbol) DO NOTHING;
                """)
                conn.execute(stmt, etf)
                print(f"Seeded: {etf['symbol']}")
            except Exception as e:
                print(f"Error seeding {etf['symbol']}: {e}")
        
        conn.commit()
    print("--- Seeding Completed ---")

if __name__ == "__main__":
    seed_tickers()
