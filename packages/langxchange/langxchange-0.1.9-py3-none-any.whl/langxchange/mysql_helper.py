import os
import pandas as pd
from dotenv import load_dotenv
import sqlalchemy
from sqlalchemy import create_engine, text


class MySQLHelper:
    def __init__(self):
         # Load environment variables from .env file
        load_dotenv()
        # Set up database connection
        self.host = os.getenv("MYSQL_HOST")
        self.db = os.getenv("MYSQL_DB")
        self.user = os.getenv("MYSQL_USER")
        self.password = os.getenv("MYSQL_PASSWORD")

        if not all([self.host, self.db, self.user, self.password]):
            raise EnvironmentError("Missing one or more required MySQL environment variables.")

        self.engine = create_engine(f"mysql+pymysql://{self.user}:{self.password}@{self.host}/{self.db}")

    def insert_dataframe(self, table_name: str, dataframe: pd.DataFrame, if_exists="append"):
        try:
            dataframe.to_sql(table_name, con=self.engine, if_exists=if_exists, index=False)
            return f"[✅ SUCCESS] Inserted {len(dataframe)} records into `{table_name}`"
        except Exception as e:
            raise RuntimeError(f"[❌ ERROR] Failed to insert data into `{table_name}`: {e}")

    def query(self, sql_query: str):
        try:
            with self.engine.connect() as conn:
                result = pd.read_sql(text(sql_query), conn)
            return result
        except Exception as e:
            raise RuntimeError(f"[❌ ERROR] Query failed: {e}")

    def execute(self, sql_command: str):
        try:
            with self.engine.connect() as conn:
                conn.execute(text(sql_command))
                conn.commit()
            return "[✅ SUCCESS] Command executed."
        except Exception as e:
            raise RuntimeError(f"[❌ ERROR] Command failed: {e}")
            
    def close(self):
        try:
            self.engine.dispose()
            return "[✅ SUCCESS] MySQL connection closed."
        except Exception as e:
            raise RuntimeError(f"[❌ ERROR] Failed to close MySQL connection: {e}")