import pandas as pd
from sqlalchemy import create_engine

def sqldf(sql: str) -> pd.DataFrame:
    sqlengine = create_engine('postgresql+psycopg2://postgres:lise890@localhost:5432/iddrs')
    return pd.read_sql(sql, sqlengine)