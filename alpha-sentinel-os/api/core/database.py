# Database Connection and Session Management
import os
import psycopg2

def get_db_connection():
    return psycopg2.connect(os.environ.get("DATABASE_URL"))
