import sqlite3

conn = sqlite3.connect("bot.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    free_used INTEGER DEFAULT 0,
    balance INTEGER DEFAULT 0
)
""")

conn.commit()