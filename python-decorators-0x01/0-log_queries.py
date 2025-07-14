import sqlite3
import functools
from datetime import datetime  # Required for logging timestamp

# Decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get('query')
        if not query and len(args) > 0:
            query = args[0]
        
        # Log timestamp and query
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if query:
            print(f"[{timestamp}] Executing SQL query: {query}")
        else:
            print(f"[{timestamp}] No SQL query provided.")
        
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Example usage
users = fetch_all_users(query="SELECT * FROM users")
print(users)
