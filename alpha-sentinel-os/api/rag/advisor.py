from typing import List, Dict
import json
import os
import sys

# 상위 모듈 접근
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from api.agents.state import AgentState
from api.agents.graph import build_graph # Macro Sentry 결과 재사용
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

def get_market_status():
    """
    현재 Alpha Sentinel 시스템이 판단한 시장 상황(Macro Sentry)을 가져옴
    """
    try:
        app = build_graph()
        result = app.invoke({"messages": [], "macro_indicators": {}, "market_prices": {}})
        return {
            "risk_level": result.get("market_risk", "NEUTRAL"),
            "risk_score": result.get("risk_score", 5.0),
            "reason": result.get("messages", [])[0] if result.get("messages") else "N/A"
        }
    except Exception as e:
        print(f"Failed to get market status: {e}")
        return {"risk_level": "NEUTRAL", "reason": "System Error"}

def generate_advice(portfolio: List[Dict], market_status: Dict):
    """
    포트폴리오와 시장 상황을 종합하여 장기 투자 조언 생성
    """
    
    # 포트폴리오 요약 문자열 생성
    port_summary = "\n".join([
        f"- {item.get('symbol', 'Unknown')}: {item.get('return_pct', 0)}% profit"
        for item in portfolio
    ])
    
    prompt = f"""
    You are a Long-Term Investment Advisor (like Warren Buffett or Ray Dalio).
    Your goal is to help the user build a wealthy, stable portfolio over 10+ years.
    
    [Current Market Condition]
    - Status: {market_status['risk_level']} (Risk Score: {market_status.get('risk_score', 'N/A')}/10)
    - Agent's View: {market_status['reason']}
    
    [User Portfolio]
    {port_summary}
    
    [Instructions]
    1. Analyze the portfolio balance. Is it too concentrated?
    2. Based on the Market Status ({market_status['risk_level']}), suggest asset allocation actions.
       - If Risk-Off: Suggest more cash/bonds or defensive sectors.
       - If Risk-On: Encourge holding quality assets.
    3. Do NOT focus on short-term price movements or technicals (RSI, charts). Focus on MACRO and FUNDAMENTALS.
    4. Provide specific, actionable advice in bullet points.
    
    Output Format:
    ## 🛡️ Portfolio Diagnosis
    (Your overall check)
    
    ## 🧭 Action Plan
    (Specific advice based on macro status)
    """
    
    response = llm.invoke([
        SystemMessage(content="You are a wise, long-term wealth manager."),
        HumanMessage(content=prompt)
    ])
    
    return response.content

if __name__ == "__main__":
    # Test Data (가짜 파싱 데이터)
    test_portfolio = [
        {"symbol": "TSLA", "quantity": 10, "return_pct": 120.5},
        {"symbol": "TQQQ", "quantity": 50, "return_pct": -15.2}
    ]
    
    print("--- Getting Market Status ---")
    status = get_market_status()
    print(f"Market: {status['risk_level']}")
    
    print("\n--- Generating Advice ---")
    advice = generate_advice(test_portfolio, status)
    print(advice)
