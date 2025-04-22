from datetime import datetime

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
            cur.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    task VARCHAR(50) NOT NULL,
                    data VARCHAR(100) NOT NULL,
                    description VARCHAR(150) NOT NULL,
                    user_id INTEGER NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
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
            except psycopg2.errors.UniqueViolation:
                self.conn.rollback()
                return False

    def check_user(self, username, password):
        with self.conn.cursor() as cur:
            cur.execute(
                sql.SQL("SELECT 1 FROM users WHERE username = %s AND password = %s"),
                (username, password)
            )
            return cur.fetchone() is not None

    def create_task(self, task, data, description, user_id):
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    sql.SQL("INSERT INTO tasks (task, data, description, user_id) VALUES (%s, %s, %s, %s)"),
                    (task, data, description, user_id)
                )
                self.conn.commit()
                return True
            except psycopg2.errors.UniqueViolation:
                self.conn.rollback()
                return False

    def check_task(self, task, data, description):
        with self.conn.cursor() as cur:
            cur.execute(
                sql.SQL("SELECT 1 FROM tasks WHERE task = %s AND data = %s AND description = %s"),
                (task, data, description)
            )
            return cur.fetchone() is not None

    def get_user_id(self, username):
        with self.conn.cursor() as cur:
            cur.execute("SELECT id FROM users WHERE username = %s", (username,))
            result = cur.fetchone()
            return result[0] if result else None

    def get_tasks_by_user_id(self, user_id):
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT task, data, description FROM tasks WHERE user_id = %s",
                (user_id,)
            )
            results = cur.fetchall()
            tasks = []
            for task, data, description in results:
                try:
                    deadline = datetime.strptime(data, '%Y-%m-%d')
                    diff_days = (deadline - datetime.now()).days
                except ValueError:
                    diff_days = 0  # Если дата невалидна
                tasks.append({
                    'text': task,
                    'deadline': data,
                    'description': description,
                    'days_left': diff_days,
                    'completed': False,
                    'height': 180
                })
            return tasks

    def close(self):
        self.conn.close()
