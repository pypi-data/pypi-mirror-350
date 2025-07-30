import pandas as pd
import mysql.connector
from sqlalchemy import create_engine


def load_csv(path, **kwargs):
    return pd.read_csv(path, **kwargs)


def load_excel(path, sheet_name=0, **kwargs):
    return pd.read_excel(path, sheet_name=sheet_name, **kwargs)


def load_sql(query, connection_string):
    engine = create_engine(connection_string)
    with engine.connect() as conn:
        return pd.read_sql(query, conn)
