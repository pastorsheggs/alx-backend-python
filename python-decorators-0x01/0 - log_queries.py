import sqlite3
import functools

# Decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get('query')
        if not query and len(args) > 0:
            query = args[0]
        if query:
            print(f"Executing SQL query: {query}")
        else:
            print("No SQL query provided.")
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
