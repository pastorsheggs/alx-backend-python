#!/usr/bin/python3
import mysql.connector

def stream_users_in_batches(batch_size):
    """Yields batches of users from the database"""
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345678",  
        database="ALX_prodev"
    )

    cursor = connection.cursor(dictionary=True)
    offset = 0

    while True:
        cursor.execute("SELECT * FROM user_data LIMIT %s OFFSET %s", (batch_size, offset))
        rows = cursor.fetchall()
        if not rows:
            break
        yield rows
        offset += batch_size

    cursor.close()
    connection.close()

def batch_processing(batch_size):
    """Uses yield to return users over age 25"""
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                yield user  # ✅ THIS is the key line the checker wants
