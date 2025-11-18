from sqlalchemy import create_engine, text
import pandas as pd

# Create SQLAlchemy engine
engine = create_engine("postgresql+psycopg2://postgres:Anjumara%401@localhost:5432/inventory_db")

def fetch_data(query, params= None):
    if params:
        # Use text() for parameterized queries with SQLAlchemy
        return pd.read_sql(text(query), engine, params=params)
    else:
        return pd.read_sql(text(query), engine)
