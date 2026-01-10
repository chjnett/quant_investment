from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from typing import Dict
import os
import sys

# 상위 폴더 모듈 접근용
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from api.agents.state import AgentState
from api.db_utils import get_db_engine
from sqlalchemy import text
from dotenv import load_dotenv

load_dotenv()

# LLM 초기화 
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def fetch_macro_data() -> Dict[str, float]:
    """DB에 저장된 가장 최신 FRED 데이터 5개를 가져옴"""
    engine = get_db_engine()
    if not engine: return {}
    
    indicators = {}
    target_series = ["FEDFUNDS", "UNRATE", "DGS10", "T10Y2Y", "VIXCLS"]
    
    with engine.connect() as conn:
        for series in target_series:
            # 가장 최근 값 1개 조회
            query = text("""
                SELECT value FROM macro_economic 
                WHERE indicator_name = :series 
                ORDER BY date DESC LIMIT 1
            """)
            result = conn.execute(query, {"series": series}).fetchone()
            if result:
                indicators[series] = float(result[0])
            else:
                indicators[series] = -1.0 # 데이터 없음
                
    return indicators

def macro_analysis_node(state: AgentState) -> AgentState:
    """
    [Macro Sentry Node]
    경제 지표를 보고 현재 시장이 'Risk-On'인지 'Risk-Off'인지 판단
    """
    print(f"--- Macro Sentry Node Starting ---")
    
    # 1. 최신 데이터 조회
    data = fetch_macro_data()
    state["macro_indicators"] = data
    
    # 2. LLM에게 판단 요청 (프롬프트 엔지니어링)
    # 장단기 금리차(T10Y2Y)가 음수이거나 실업률이 급등하면 위험 신호
    prompt = f"""
    You are an aggressive Growth Strategist. Your goal is to find investment opportunities even in challenging markets.
    Do NOT store cash unless the market is facing an immediate crash (e.g., Financial Crisis level).
    
    Current Indicators:
    - Fed Funds Rate: {data.get('FEDFUNDS', 'N/A')}%
    - Unemployment Rate: {data.get('UNRATE', 'N/A')}%
    - 10Y Treasury Yield: {data.get('DGS10', 'N/A')}%
    - 10Y-2Y Spread: {data.get('T10Y2Y', 'N/A')} (Negative is a warning, but not a stop signal if VIX is low)
    - VIX (Fear Index): {data.get('VIXCLS', 'N/A')}
    
    Decision Rules:
    1. If VIX is below 20, lean towards 'RISK_ON' or 'NEUTRAL'.
    2. Even if the Yield Curve (T10Y2Y) is negative, if Unemployment is stable (< 5.0%), consider it 'NEUTRAL'.
    3. Only declare 'RISK_OFF' if multiple indicators are flashing red simultaneously (e.g., VIX > 30 AND Unemployment spiking).
    
    Classify the market status:
    1. 'RISK_ON' (Aggressive Buy)
    2. 'NEUTRAL' (Buy with caution / Sector rotation)
    3. 'RISK_OFF' (Cash is king)
    
    Output Format: RISK_LEVEL | SCORE | REASON
    Example: NEUTRAL | 4.5 | Yield curve inverted but VIX is low, suggesting a soft landing.
    """
    
    response = llm.invoke([SystemMessage(content="You are an aggressive growth strategist. Prioritize opportunity over safety."), HumanMessage(content=prompt)])
    content = response.content.strip()
    
    # 3. LLM 응답 파싱
    try:
        parts = content.split(" | ")
        risk_level = parts[0].strip()
        risk_score = float(parts[1].strip())
        reason = parts[2].strip()
    except:
        # 파싱 실패 시 기본값 (안전제일)
        risk_level = "NEUTRAL"
        risk_score = 5.0
        reason = "Parsing failed, defaulted to Neutral."
        
    print(f"Decision: {risk_level} (Score: {risk_score})")
    print(f"Reason: {reason}")
    
    # State 업데이트
    state["market_risk"] = risk_level
    state["risk_score"] = risk_score
    state["messages"].append(f"[Macro] {risk_level}: {reason}")
    
    return state
