from langgraph.graph import StateGraph, END
import sys
import os
from dotenv import load_dotenv

# 상위 폴더 모듈 접근용
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from api.agents.state import AgentState
from api.agents.macro_node import macro_analysis_node

load_dotenv()

def build_graph():
    """LangGraph 워크플로우 정의"""
    workflow = StateGraph(AgentState)

    # 1. 노드 추가
    workflow.add_node("macro_sentry", macro_analysis_node)

    # 2. 엣지 연결 (Start -> Macro -> End)
    # 지금은 테스트라 바로 끝내지만, 나중엔 Sector -> CIO로 이어짐
    workflow.set_entry_point("macro_sentry")
    workflow.add_edge("macro_sentry", END)

    # 3. 컴파일
    app = workflow.compile()
    return app

if __name__ == "__main__":
    print("🚀 [Alpha Sentinel Agent] Starting...")
    
    # 그래프 빌드
    app = build_graph()
    
    # 초기 상태 (빈 값)
    initial_state = {
        "messages": [],
        "macro_indicators": {},
        "market_prices": {}
    }
    
    # 실행
    result = app.invoke(initial_state)
    
    print("\n🏁 [Result Summary]")
    print(f"Risk Level: {result.get('market_risk')}")
    print(f"Risk Score: {result.get('risk_score')}")
    print(f"Messages: {result.get('messages')}")
