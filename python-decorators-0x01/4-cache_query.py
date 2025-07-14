import time
import sqlite3
import functools

# Global query cache
query_cache = {}

# Connection handling decorator
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# Caching decorator
def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        # Get the query string from positional or keyword args
        query = kwargs.get('query')
        if query is None and len(args) > 0:
            query = args[0]  # If query passed positionally

        # Check cache
        if query in query_cache:
            print("Returning cached result.")
            return query_cache[query]

        # Execute query and cache it
        result = func(conn, *args, **kwargs)
        query_cache[query] = result
        print("Query executed and cached.")
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

# Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")

print(users_again)
