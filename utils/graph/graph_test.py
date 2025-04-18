from dotenv import load_dotenv
from pathlib import Path
env_path = Path(__file__).resolve().parents[2] / '.env'
load_dotenv(dotenv_path=env_path)


from pathlib import Path

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import streamlit as st
import pandas as pd
from datetime import datetime

from utils.graph.graph1 import KeywordVisualization  # 방금 만든 클래스 경로


visualizer = KeywordVisualization()


selected_date = st.date_input("날짜를 선택하세요", datetime.today())
selected_date_str = selected_date.strftime("%Y-%m-%d")


selected_keyword = st.text_input("추이 확인할 키워드를 입력하세요", "예시키워드")


sql = "SELECT * FROM word_list"
df = visualizer.db.fetch_df(sql)


if st.button("히트맵 보기"):
    visualizer.visualize_heatmap(df)

if st.button("바 차트 보기"):
    visualizer.bar_chart(df, selected_date_str)

if st.button("라인 차트 보기"):
    visualizer.line_chart(df, selected_keyword)