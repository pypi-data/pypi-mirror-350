import os
import pytest
import pandas as pd
from sqlalchemy import create_engine, text
from langxchange.mysql_helper import MySQLHelper


@pytest.fixture(scope="module")
def mysql_helper():
    #setup MySQL connection Environment variables
    os.environ["MYSQL_HOST"] = "localhost"
    os.environ["MYSQL_USER"] = "testuser"
    os.environ["MYSQL_PASSWORD"] = "testpassword"
    os.environ["MYSQL_DB"] = "testdb"      
    # Make sure these environment variables are set before running the test
    host = os.getenv("MYSQL_HOST", "localhost")
    user = os.getenv("MYSQL_USER", "testuser")
    password = os.getenv("MYSQL_PASSWORD", "testpassword")
    db = os.getenv("MYSQL_DB", "testdb")

    engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{db}")
    
    with engine.begin() as conn:
        conn.execute(text("CREATE TABLE IF NOT EXISTS test_table (id INT, name VARCHAR(50))"))
        conn.execute(text("TRUNCATE TABLE test_table"))
        conn.execute(text("INSERT INTO test_table VALUES (1, 'Alice'), (2, 'Bob')"))

    return MySQLHelper()

def test_execute_query(mysql_helper):
    df = mysql_helper.query("SELECT * FROM test_table")
    assert isinstance(df, pd.DataFrame)
    assert df.shape[0] == 2  # ✅ Should match inserted rows
    assert list(df.columns) == ["id", "name"]

def test_bad_query(mysql_helper):
    with pytest.raises(Exception):
        mysql_helper.query("SELECT * FROM non_existing_table")
