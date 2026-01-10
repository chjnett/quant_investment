from typing import TypedDict, List, Dict, Optional, Annotated
import operator

class AgentState(TypedDict):
    """
    LangGraph에서 에이전트 간에 공유되는 상태(State) 정의
    """
    
    # 1. 원본 데이터 (Raw Data)
    macro_indicators: Dict[str, float]  # 경제지표 (예: {"FEDFUNDS": 5.33, "UNRATE": 4.1})
    market_prices: Dict[str, float]     # 주요 자산 가격 (예: {"SPY": 500.1, "BTC": 65000})

    # 2. 분석 결과 (Analysis)
    market_risk: str  # 'RISK_ON', 'RISK_OFF', 'NEUTRAL' 
    risk_score: float # 0.0 (Safe) ~ 10.0 (Danger)
    
    # 3. 투자 가설 (Investment Thesis)
    target_sectors: List[str] # 유망 섹터 (예: ["Tech", "Healthcare"])
    
    # 4. 최종 메시지
    messages: Annotated[List[str], operator.add] # 로그/메시지 누적
