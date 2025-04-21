import streamlit as st
st.set_page_config(page_title="키워드 분석 대시보드", layout="wide")
from pathlib import Path
import sys
import os


import pandas as pd
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[1]  
sys.path.append(str(BASE_DIR))

from utils.graph.graph1 import KeywordVisualization  
from dotenv import load_dotenv
from pathlib import Path


# 환경 변수 로드
env_path = Path(__file__).resolve().parents[2] / '.env'
load_dotenv(dotenv_path=env_path)

# 경로 설정
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# 시각화 클래스 인스턴스 생성
visualizer = KeywordVisualization()



st.title(" 분석 페이지")


# 데이터 조회
sql = "SELECT * FROM word_list"
df = visualizer.db.fetch_df(sql)

#  경로 설정
BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR))

#  시각화 클래스 불러오기
from utils.graph.graph1 import KeywordVisualization

#  인스턴스 생성
visualizer = KeywordVisualization()

# DB에서 데이터 불러오기
sql = "SELECT * FROM word_list"
df = visualizer.db.fetch_df(sql)

#  오늘 날짜 문자열
today_str = datetime.today().strftime("%Y-%m-%d")


if not df.empty:
    # 날짜 선택
    selected_date = st.date_input("날짜를 선택하세요", datetime.today())
    selected_date_str = selected_date.strftime("%Y-%m-%d")

    # 오늘 기준 상위 키워드
    today_df = df[df['append_date'] == today_str]
    top_keywords = today_df.sort_values(by='append_count', ascending=False)['append_word'].tolist()
    default_keyword = top_keywords[0] if top_keywords else "AI"

    # 키워드 선택
    keyword_input = st.selectbox(
        "확인할 키워드를 선택하세요",
        options=df['append_word'].unique(),
        index=df['append_word'].tolist().index(default_keyword) if default_keyword in df['append_word'].tolist() else 0
    )

    # 1행
    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        st.subheader("히트맵")
        visualizer.visualize_heatmap(df)

    with row1_col2:
        st.subheader("바 차트")
        visualizer.bar_chart(df, selected_date_str)

    # 2행
    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:
        st.subheader(f"라인 차트 - 키워드: {keyword_input}")
        visualizer.line_chart(df, keyword_input)

    with row2_col2:
        st.subheader("워드 클라우드 (최근 7일)")
        visualizer.generate_wordcloud_last_week()

else:
    st.warning("데이터가 비어 있어요. 먼저 데이터를 확인해주세요.")
        
#   streamlit run MiniProject1\pages\분석페이지.py