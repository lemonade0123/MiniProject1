import streamlit as st
from sqlalchemy import create_engine, text
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()


class Database:
    def __init__(self):
        
        self.engine = create_engine(
            os.getenv("DATABASE_URL"),
            pool_size=5,
            max_overflow=2,
            pool_recycle=1800,
            pool_pre_ping=True
        )
        
    def fetch_df(self, query: str, params: dict = None):
        with self.engine.connect() as conn:
            result = conn.execute(text(query), params or {})
            df = pd.DataFrame(result.fetchall(), columns=result.keys())
            return df

    def execute(self, query: str, params: dict = None):
        with self.engine.connect() as conn:
            conn.execute(text(query), params or {})
            conn.commit()
            
    def insert(self, table_name:str, data:dict):
        if isinstance(data, dict):
                data = [data]  # 단일 row도 리스트로 변환

        if not data:
            return  # 빈 리스트면 아무 것도 하지 않음

        columns = ', '.join(data[0].keys())
        placeholders = ', '.join([f":{key}" for key in data[0].keys()])
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        with self.engine.connect() as conn:
            conn.execute(text(query), data)  # 리스트 넘기면 다건 처리됨
            conn.commit()
        

#  연결 재사용을 위한 캐싱 처리리
@st.cache_resource
def get_db():
   
    return Database()


## 테스트 코드
# db = get_db()
# users_df = db.fetch_df("SELECT * FROM product")
# print(users_df)
# st.dataframe(users_df)
