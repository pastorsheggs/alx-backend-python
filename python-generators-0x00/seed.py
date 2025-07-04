#!/usr/bin/python3
import mysql.connector
import csv
import uuid

DB_NAME = "ALX_prodev"

# Connect to MySQL server (no specific DB yet)
def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""  # or your MySQL root password
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Create the ALX_prodev database if it doesn't exist
def create_database(connection):
    cursor = connection.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME};")
    connection.commit()
    cursor.close()

# Connect directly to ALX_prodev database
def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # or your MySQL root password
            database=DB_NAME
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Create the user_data table with required fields
def create_table(connection):
    cursor = connection.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id CHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL NOT NULL,
        INDEX(user_id)
    );
    """
    cursor.execute(create_table_query)
    connection.commit()
    cursor.close()
    print("Table user_data created successfully")

# Insert data from CSV if not already present
def insert_data(connection, csv_file):
    cursor = connection.cursor()
    with open(csv_file, newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            user_id, name, email, age = row
            # Check if user already exists
            cursor.execute("SELECT user_id FROM user_data WHERE user_id = %s", (user_id,))
            if not cursor.fetchone():
                cursor.execute(
                    "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
                    (user_id, name, email, age)
                )
    connection.commit()
    cursor.close()
