import os
import psycopg2
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 1. 환경 변수에서 DATABASE_URL 가져오기
        db_url = os.environ.get('DATABASE_URL')
        
        try:
            # 2. DB 연결 시도
            conn = psycopg2.connect(db_url, sslmode='require')
            cur = conn.cursor()
            
            # 3. 간단한 쿼리 실행 (DB 버전 확인)
            cur.execute("SELECT version();")
            db_version = cur.fetchone()
            
            # 4. 아까 만든 테이블이 존재하는지 확인
            cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
            tables = cur.fetchall()
            
            cur.close()
            conn.close()

            self.send_response(200)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            
            response = f"✅ 연결 성공!\nDB 버전: {db_version[0]}\n존재하는 테이블: {[t[0] for t in tables]}"
            self.wfile.write(response.encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"❌ 연결 실패: {str(e)}".encode('utf-8'))