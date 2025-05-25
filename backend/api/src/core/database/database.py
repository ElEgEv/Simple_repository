import sqlite3
import os
from config import Config
from src.utils.custom_logging import setup_logging

config = Config()
log = setup_logging()


class Database:
    def __init__(self):
        db_path = config.__getattr__("DB_NAME")
        db_exists = os.path.exists(db_path)

        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = sqlite3.Row

        if not db_exists:
            self._initialize_database()

    def _initialize_database(self):
        try:
            # Построение абсолютного пути к create_sql.sql
            base_dir = os.path.dirname(os.path.abspath(__file__))  # Папка с database.py
            script_path = os.path.join(base_dir, "../../../create_sql.sql")
            script_path = os.path.normpath(script_path)

            with open(script_path, "r", encoding="utf-8") as f:
                sql_script = f.read()

            self.connection.executescript(sql_script)
            self.connection.commit()
            log.info("База данных успешно инициализирована.")
        except Exception as e:
            log.exception("Ошибка при инициализации базы данных: %s", e)

    def check_and_reconnect(self):
        try:
            self.connection.close()
            self.connection = sqlite3.connect(config.__getattr__("DB_NAME"))
            self.connection.row_factory = sqlite3.Row
        except sqlite3.OperationalError as e:
            log.exception(e)

    def execute_query(self, query, params=None):
        self.check_and_reconnect()
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(query, params or [])
            return cursor

    def fetch_one(self, query, params=None):
        self.check_and_reconnect()
        cursor = self.connection.cursor()
        cursor.execute(query, params or [])
        result = cursor.fetchone()
        cursor.close()
        return result

    def fetch_all(self, query, params=None):
        self.check_and_reconnect()
        cursor = self.connection.cursor()
        cursor.execute(query, params or [])
        results = cursor.fetchall()
        cursor.close()
        return results


db = Database()
