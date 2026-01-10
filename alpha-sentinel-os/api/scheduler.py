import time
import schedule
import subprocess
import os
import sys
from datetime import datetime

# 파이썬 실행 명령어 (도커 내부)
PYTHON_CMD = "python"

def run_job(module_name, description):
    """지정된 파이썬 모듈을 -m 모드로 실행"""
    print(f"\n⏰ [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting Job: {description}")
    try:
        # python -m api.collectors.market 형태
        cmd = [PYTHON_CMD, "-m", module_name]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Success ({description}):\n{result.stdout[:200]}...") # 로그 너무 길면 자름
        else:
            print(f"❌ Failed ({description}):\n{result.stderr}")
            
    except Exception as e:
        print(f"❌ Error running {module_name}: {e}")

def daily_routine():
    """매일 실행되는 전체 파이프라인 루틴"""
    print("=== 🚀 Daily Pipeline Started ===")
    
    # 1. FRED 거시경제 지표 수집
    run_job("api.collectors.fred", "Macro Data Collection")
    
    # 2. 주식/ETF 시세 수집
    run_job("api.collectors.market", "Market Data Collection")
    
    # 3. Macro Sentry & Sector Strategist 실행 (Graph)
    # 이 단계에서 AI가 판단하고 DB/로그에 결과를 남김
    run_job("api.agents.graph", "AI Strategy Analysis")
    
    print("=== 🏁 Daily Pipeline Finished ===")

def run_scheduler():
    print("🕒 Scheduler Started. Waiting for scheduled jobs...")
    
    # 테스트용: 시작하자마자 1회 실행 (개발 중 편의를 위해)
    daily_routine()
    
    # 미국 장 시작 전 (한국 시간 밤 10시) 실행
    schedule.every().day.at("22:00").do(daily_routine)
    
    # 장 마감 후 (한국 시간 아침 6시 30분) 실행 - 데이터 확정용
    schedule.every().day.at("06:30").do(daily_routine)

    while True:
        schedule.run_pending()
        time.sleep(60) # 1분마다 체크

if __name__ == "__main__":
    run_scheduler()
