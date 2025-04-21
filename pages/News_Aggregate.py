import streamlit as st
from pathlib import Path
import sys
import os
import pandas as pd
from datetime import datetime, timedelta

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

        if not df.empty:
            # 날짜 컬럼을 datetime 형식으로 변환
            df['append_date'] = pd.to_datetime(df['append_date'])

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### 시작 날짜")
                start_date = st.date_input(label="",value=datetime.today() - timedelta(days=6))
            with col2:
                st.markdown("#### 종료 날짜")
                end_date = st.date_input(label="",value=datetime.today())

            # 날짜 범위 필터링
            mask = (df['append_date'] >= pd.to_datetime(start_date)) & (df['append_date'] <= pd.to_datetime(end_date))
            range_df = df.loc[mask]

            if not range_df.empty:
                # 기본 키워드 설정
                top_keywords = range_df.sort_values(by='append_count', ascending=False)['append_word'].tolist()
                default_keyword = top_keywords[0] if top_keywords else "AI"

                # 바 차트
                st.subheader("📊 키워드 통계")
                self.visualizer.bar_chart(df, start_date, end_date)

                # 워드클라우드 + 키워드 선택
                col1, col2 = st.columns([1, 1])

                with col1:
                    st.markdown("")
                    st.subheader("유행 단어")
                    self.visualizer.generate_wordcloud_last_week()

                with col2:
                    keyword_sql = "select append_word , sum(append_count) from word_list group by append_word order by sum(append_count) desc"
                    keyword_df = self.visualizer.db.fetch_df(keyword_sql)
                    
                    
                    st.markdown("")
                    st.subheader(" 📈 단어별 통계 ")
                    keyword_input = st.selectbox(
                    label="키워드 선택",
                    options=keyword_df['append_word'].unique(),
                    index=keyword_df['append_word'].tolist().index(default_keyword) if default_keyword in keyword_df['append_word'].tolist() else 0
                    )

                    
                    self.visualizer.line_chart(df, keyword_input)

            else:
                st.warning("선택한 기간에 해당하는 데이터가 없습니다.")

        else:
            st.warning("데이터가 비어 있어요. 먼저 데이터를 확인해주세요.")
render_sidebar()
render_layout("📰 통계 페이지", NewsAggregate().get_content)
