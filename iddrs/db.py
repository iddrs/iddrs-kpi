"""Funções para iteração com o banco de dados"""
import pandas as pd

from iddrs import config
from iddrs import db
from sqlalchemy import create_engine

def get_engine():
    """
    Inicia uma conexão com o banco de dados.
    :return: Engine do SQLAlchemy
    """
    return create_engine(config.engine_connection_string)

def load_df(table_name, schema):
    engine = db.get_engine()
    conn = engine.connect()
    df = pd.read_sql_query(f'SELECT * FROM {schema}."{table_name}"', conn)
    conn.close()
    return df

def exec_sql(sql):
    engine = db.get_engine()
    conn = engine.connect()
    df = pd.read_sql_query(sql, conn)
    conn.close()
    return df