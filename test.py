# test.py
import os
import psycopg2

def test_connection_to_db():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "geodata"),
        user=os.getenv("DB_USER", "roger"),
        password=os.getenv("DB_PASSWORD", "motdepassefort")
    )
    cursor = conn.cursor()
    cursor.execute("SELECT 1;")
    assert cursor.fetchone()[0] == 1
    cursor.close()
    conn.close()
