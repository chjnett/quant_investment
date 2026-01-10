from typing import List, Dict, Tuple
from sqlalchemy import text
import pandas as pd
import sys
import os

# 상위 모듈 접근
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from api.agents.state import AgentState
from api.db_utils import get_db_engine

# 분석 대상 섹터 매핑 (Symbol -> Sector Name)
SECTOR_MAP = {
    "XLK": "Technology",
    "XLV": "Healthcare",
    "XLF": "Financial",
    "XLY": "Consumer Discretionary",
    "XLP": "Consumer Staples",
    "XLE": "Energy",
    "XLI": "Industrial",
    "XLB": "Materials",
    "XLU": "Utilities",
    "XLRE": "Real Estate",
    "XLC": "Communication Services"
}

def get_sector_momentum(engine) -> List[Tuple[str, float]]:
    """
    각 섹터 ETF의 최근 모멘텀(수익률)을 계산하여 순위 반환
    모멘텀 로직: (1개월 수익률 * 0.3) + (3개월 수익률 * 0.3) + (6개월 수익률 * 0.4)
    """
    rankings = []
    
    with engine.connect() as conn:
        for symbol, sector_name in SECTOR_MAP.items():
            # 최근 데이터 가져오기 (약 6개월 = 130 trading days)
            query = text("""
                SELECT m.date, m.close 
                FROM market_data m
                JOIN tickers t ON m.ticker_id = t.id
                WHERE t.symbol = :symbol
                ORDER BY m.date DESC
                LIMIT 130
            """)
            df = pd.read_sql(query, conn, params={"symbol": symbol})
            
            if len(df) < 120: continue # 데이터 부족하면 스킵
            
            # 날짜 오름차순 정렬 (과거 -> 현재)
            df = df.sort_values("date").reset_index(drop=True)
            
            current_price = df.iloc[-1]['close']
            
            # 수익률 계산 (데이터가 존재할 경우만)
            try:
                ret_1m = (current_price / df.iloc[-20]['close']) - 1 # 약 1달 전
                ret_3m = (current_price / df.iloc[-60]['close']) - 1 # 약 3달 전
                ret_6m = (current_price / df.iloc[-120]['close']) - 1 # 약 6달 전
                
                # 가중 모멘텀 점수
                score = (ret_1m * 30) + (ret_3m * 30) + (ret_6m * 40)
                rankings.append((sector_name, round(score, 2)))
                
            except IndexError:
                continue

    # 점수 높은 순 정렬
    rankings.sort(key=lambda x: x[1], reverse=True)
    return rankings

def sector_strategy_node(state: AgentState) -> AgentState:
    """
    [Sector Strategist Node]
    Macro Sentry의 판단이 'Risk-On' 또는 'Neutral'일 때 유망 섹터 발굴
    """
    print("--- Sector Strategist Node Starting ---")
    
    # 1. 시장 상황 확인 (Macro Sentry 결과)
    risk_level = state.get("market_risk", "NEUTRAL")
    
    # 2. 킬스위치: Risk-Off면 섹터 추천 안 함 (현금/채권 비중 확대 필요)
    if risk_level == "RISK_OFF":
        print("Market is Risk-Off. Skipping Sector Strategy.")
        state["messages"].append("[Sector] Market is dangerous. No sectors recommended (Cash/Bond Pref).")
        state["target_sectors"] = []
        return state

    # 3. 섹터 모멘텀 분석
    engine = get_db_engine()
    if not engine: return state
    
    rankings = get_sector_momentum(engine)
    
    if not rankings:
        print("Not enough data for sector analysis.")
        return state
        
    # 4. 상위 3개 섹터 선정
    top_3 = [r[0] for r in rankings[:3]]
    top_3_str = ", ".join([f"{r[0]}({r[1]})" for r in rankings[:3]])
    
    print(f"Top Sectors: {top_3_str}")
    
    # State 업데이트
    state["target_sectors"] = top_3
    state["messages"].append(f"[Sector] Top performing sectors: {top_3_str}")
    
    return state
