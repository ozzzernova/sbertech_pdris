from flask import Flask
import psycopg2
import os

class Config:
    DATABASE = {
        'dbname': os.getenv('POSTGRES_DB'),
        'user': os.getenv('POSTGRES_USER'),
        'password': os.getenv('POSTGRES_PASSWORD'),
        'host': os.getenv('POSTGRES_HOST'),
        'port': os.getenv('POSTGRES_PORT'),
    }

def get_db_connection():
    conn = psycopg2.connect(**Config.DATABASE)
    return conn

app = Flask(__name__)

@app.route('/')
def ping():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute('UPDATE counter SET value = value + 1 RETURNING value;')
                value = cursor.fetchone()[0]
                conn.commit()
                if value % 2 == 0:
                    return 'ping'
                else:
                    return 'pong'

    except Exception as error:
        return f'Connection error: {error}'


if __name__ == '__main__':
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS counter (
                    id SERIAL PRIMARY KEY,
                    value INTEGER NOT NULL
                )
            ''')
            conn.commit()
            
            cursor.execute('SELECT COUNT(*) FROM counter')
            if cursor.fetchone()[0] == 0:
                cursor.execute('INSERT INTO counter (value) VALUES (0)')
                conn.commit()
            
    app.run(host='0.0.0.0', port=5000)

