import os
import psycopg2

from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_db():
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    try:
        yield conn
    finally:
        conn.close()

def query(conn, sql, params=None):
    with conn.cursor() as cur:
        cur.excute(sql, params)
        return cur.fetchall()

def query_one(conn, sql, params=None):
    with conn.cursor() as cur:
        cur.excute(sql, params)
        return cur.fetchone()

def execute(conn,sql, params=None):
        with conn.cursor() as cur:
        cur.excute(sql, params)
        return cur.rowcount
          
