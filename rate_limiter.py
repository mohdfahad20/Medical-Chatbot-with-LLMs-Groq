import sqlite3
import hashlib
from datetime import datetime, timedelta
import streamlit as st

DB_PATH = "rate_limits.db"

def init_rate_limit_db():
    """Initialize SQLite database for rate limiting"""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS rate_limits
                 (user_id TEXT, timestamp REAL, PRIMARY KEY (user_id, timestamp))''')
    conn.commit()
    conn.close()

def get_user_identifier():
    """Get unique user identifier"""
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx
        ctx = get_script_run_ctx()
        if ctx:
            return hashlib.md5(ctx.session_id.encode()).hexdigest()
    except:
        pass
    
    if "user_id" not in st.session_state:
        import uuid
        st.session_state.user_id = str(uuid.uuid4())
    return st.session_state.user_id

def check_rate_limit(user_id: str, max_requests: int = 10, window_hours: int = 3):
    """
    Check if user has exceeded rate limit
    
    Returns:
        tuple: (can_proceed: bool, requests_made: int, reset_time: datetime or None)
    """
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    c = conn.cursor()
    
    now = datetime.now()
    cutoff = (now - timedelta(hours=window_hours)).timestamp()
    
    # Clean old entries
    c.execute("DELETE FROM rate_limits WHERE timestamp < ?", (cutoff,))
    conn.commit()
    
    # Count recent requests
    c.execute("""SELECT COUNT(*), MIN(timestamp) 
                 FROM rate_limits 
                 WHERE user_id = ? AND timestamp > ?""",
              (user_id, cutoff))
    
    result = c.fetchone()
    count = result[0]
    oldest_timestamp = result[1]
    
    # Calculate reset time
    reset_time = None
    if oldest_timestamp and count >= max_requests:
        oldest_time = datetime.fromtimestamp(oldest_timestamp)
        reset_time = oldest_time + timedelta(hours=window_hours)
    
    if count >= max_requests:
        conn.close()
        return False, count, reset_time
    
    # Log this request
    try:
        c.execute("INSERT INTO rate_limits VALUES (?, ?)",
                  (user_id, now.timestamp()))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    
    conn.close()
    return True, count + 1, reset_time

def get_user_stats(user_id: str, window_hours: int = 3):
    """Get user's request statistics"""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    c = conn.cursor()
    
    cutoff = (datetime.now() - timedelta(hours=window_hours)).timestamp()
    
    c.execute("""SELECT COUNT(*) FROM rate_limits 
                 WHERE user_id = ? AND timestamp > ?""",
              (user_id, cutoff))
    
    count = c.fetchone()[0]
    conn.close()
    
    return count