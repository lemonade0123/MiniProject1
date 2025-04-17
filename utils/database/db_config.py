import streamlit as st
from sqlalchemy import create_engine, text
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

#  연결 재사용을 위한 캐싱 처리리
@st.cache_resource
def get_db():
   
    return Database()