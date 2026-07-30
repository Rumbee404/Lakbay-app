import sqlite3
import os
import contextlib
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "analytics.db")

def _connect(path=DB_PATH):
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database(path=DB_PATH):
    """
    This file is responsible for our search analytics.
    Creates the database file and search_logs table if missing.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with contextlib.closing(_connect(path)) as conn:
        with conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS search_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    query TEXT NOT NULL,
                    searched_at TEXT NOT NULL,
                    result_count INTEGER NOT NULL,
                    top_result TEXT,
                    execution_time_ms REAL NOT NULL
                )
            ''')

def log_search(query, result_count, top_result, execution_time_ms, path=DB_PATH):
    """Records a search query and performance stats into the database."""
    searched_at = datetime.utcnow().isoformat()
    with contextlib.closing(_connect(path)) as conn:
        with conn:
            conn.execute('''
                INSERT INTO search_logs (query, searched_at, result_count, top_result, execution_time_ms)
                VALUES (?, ?, ?, ?, ?)
            ''', (query, searched_at, result_count, top_result, execution_time_ms))

def get_analytics_summary(path=DB_PATH):
    """Retrieves aggregated metrics for display on the analytics page."""
    with contextlib.closing(_connect(path)) as conn:
        cursor = conn.cursor()
        
        total_searches = cursor.execute('SELECT COUNT(*) FROM search_logs').fetchone()[0]
        avg_latency = cursor.execute('SELECT AVG(execution_time_ms) FROM search_logs').fetchone()[0] or 0.0
        
        top_queries = cursor.execute('''
            SELECT query, COUNT(*) as count 
            FROM search_logs 
            GROUP BY query 
            ORDER BY count DESC 
            LIMIT 5
        ''').fetchall()
        
        recent_searches = cursor.execute('''
            SELECT query, searched_at, result_count, top_result, execution_time_ms 
            FROM search_logs 
            ORDER BY id DESC 
            LIMIT 10
        ''').fetchall()
        
    return {
        "total_searches": total_searches,
        "avg_latency": round(avg_latency, 2),
        "top_queries": top_queries,
        "recent_searches": recent_searches
    }