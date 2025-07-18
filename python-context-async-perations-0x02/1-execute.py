import sqlite3

class ExecuteQuery:
    def __init__(self, query, params=None, db_file='users.db'):
        self.query = query
        self.params = params or []
        self.db_file = db_file
        self.conn = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        self.results = self.cursor.fetchall()
        return self.results

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

# Example usage
query = "SELECT * FROM users WHERE age > ?"
params = [25]

with ExecuteQuery(query, params) as results:
    print(results)
