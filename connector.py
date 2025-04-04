import psycopg2
from psycopg2 import sql

class DBConnector:
    def __init__(self, dbname="workdb", user="postgres", host="127.0.0.1", port="5432"):
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            host=host,
            port=port
        )
        self.create_tables()

    def create_tables(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(100) NOT NULL
                )
            """)
            self.conn.commit()

    def create_user(self, username, password):
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    sql.SQL("INSERT INTO users (username, password) VALUES (%s, %s)"),
                    (username, password)
                )
                self.conn.commit()
                return True
            except psycopg2.IntegrityError:  # Если пользователь уже существует
                self.conn.rollback()
                return False

    def check_user(self, username, password):
        with self.conn.cursor() as cur:
            cur.execute(
                sql.SQL("SELECT 1 FROM users WHERE username = %s AND password = %s"),
                (username, password)
            )
            return cur.fetchone() is not None

    def close(self):
        self.conn.close()