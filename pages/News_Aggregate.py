import streamlit as st
from pathlib import Path
import sys
import os
import pandas as pd
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[1]  
sys.path.append(str(BASE_DIR))

#  시각화 클래스 불러오기
from utils.graph.graph1 import KeywordVisualization 
from pathlib import Path

from components.sidebar import render_sidebar
from components.layout import render_layout

# 경로 설정
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

class NewsAggregate:
    def __init__(self):
        self.visualizer = KeywordVisualization()
        
        
    def get_content(self):
    # 데이터 조회
        sql = "SELECT * FROM word_list"
        df = self.visualizer.db.fetch_df(sql)

        today_str = datetime.today().strftime("%Y-%m-%d")

        if not df.empty:
            # 날짜 선택
            selected_date = st.date_input("날짜를 선택하세요", datetime.today())
            selected_date_str = selected_date.strftime("%Y-%m-%d")

            # 오늘 기준 상위 키워드
            today_df = df[df['append_date'] == today_str]
            top_keywords = today_df.sort_values(by='append_count', ascending=False)['append_word'].tolist()
            default_keyword = top_keywords[0] if top_keywords else "AI"

            # 바 차트 (1행 전체)
            st.subheader("바 차트")
            self.visualizer.bar_chart(df, selected_date_str)

            # 2행: 워드클라우드 + 키워드 선택 + 라인 차트
            col1, col2 = st.columns([2, 2])

            with col1:
                st.subheader("워드클라우드 (최근 7일)")
                self.visualizer.generate_wordcloud_last_week()

            with col2:
                
                keyword_input = st.selectbox(
                    label="키워드 선택",
                    options=df['append_word'].unique(),
                    index=df['append_word'].tolist().index(default_keyword) if default_keyword in df['append_word'].tolist() else 0
                )

                st.subheader(f"라인 차트 - 키워드: {keyword_input}")
                self.visualizer.line_chart(df, keyword_input)

        else:
            st.warning("데이터가 비어 있어요. 먼저 데이터를 확인해주세요.")

render_sidebar()
render_layout("📰 통계 페이지", NewsAggregate().get_content)
