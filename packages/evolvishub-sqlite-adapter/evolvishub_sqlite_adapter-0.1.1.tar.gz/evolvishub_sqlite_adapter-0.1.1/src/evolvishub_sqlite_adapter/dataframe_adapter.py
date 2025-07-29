import sqlite3
import pandas as pd

class SQLiteDataFrameAdapter:
    def __init__(self, db_path):
        if not db_path:
            raise ValueError("Database path must be provided.")
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    def create_table(self, query):
        if not query:
            raise ValueError("Query must be provided.")
        self.conn.execute(query)
        self.conn.commit()

    def execute_query(self, query, params=None):
        if not query:
            raise ValueError("Query must be provided.")
        if params is None:
            self.conn.execute(query)
        else:
            self.conn.execute(query, params)
        self.conn.commit()

    def fetch_dataframe(self, query):
        if not query:
            raise ValueError("Query must be provided.")
        return pd.read_sql_query(query, self.conn) 