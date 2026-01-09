import os
from sqlalchemy import create_engine

# DB 연결 정보 (환경변수 또는 기본값)
# 로컬 테스트 시 localhost 자동 변환 로직 포함
DB_URL = os.getenv("DATABASE_URL", "postgresql://chj:qwer@db:5432/alpha_sentinel")
if "localhost" in DB_URL and os.path.exists('/.dockerenv'):
     DB_URL = DB_URL.replace("localhost", "db")

def get_db_engine():
    """SQLAlchemy 엔진 객체 반환"""
    try:
        engine = create_engine(DB_URL)
        return engine
    except Exception as e:
        print(f"❌ DB 연결 실패: {e}")
        return None
