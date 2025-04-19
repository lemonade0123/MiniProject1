import streamlit as st
import os
from dotenv import load_dotenv
from datetime import date

load_dotenv()

def render_sidebar():
    with st.sidebar:
        # --- 로고 (필요시 주석 해제) ---
        # st.image("assets/logo.png", use_column_width=True)
        st.markdown("---")

        # --- 버튼 스타일 ---
        st.markdown("""
            <style>
            section[data-testid="stSidebar"] button {
                width: 100% !important;
                height: 50px;
                font-size: 18px;
                border-radius: 8px;
                background-color: #4CAF50;
                color: white;
            }
            section[data-testid="stSidebar"] button:hover {
                background-color: #45a049;
            }
            </style>
        """, unsafe_allow_html=True)

        # --- 분석 페이지 이동 버튼 ---
        if st.button("📊 분석 페이지로 이동"):
            st.switch_page("pages/News_Aggregate.py")

        st.markdown("---")
        st.subheader("🔍 고급 검색")

        # --- 날짜 범위 선택 ---
        start_date, end_date = st.date_input(
            "날짜 범위 선택",
            value=(date.today(), date.today())
        )

        # --- 키워드 입력 ---
        keyword = st.text_input("검색어 입력", placeholder="검색어를 입력하세요")

        st.markdown("---")

        # --- 값 리턴 ---
        return start_date, end_date, keyword
