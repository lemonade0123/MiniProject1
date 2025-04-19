import streamlit as st
import os
from dotenv import load_dotenv
<<<<<<< HEAD
from datetime import datetime, date
import random
=======

>>>>>>> origin/feature/NEWS-007
# --- 컴포넌트 및 스크래퍼 임포트 ---
from components.sidebar import render_sidebar
from utils.web_scrap.web_scrapping_han import HaniEconomyScraper
from utils.web_scrap.web_scrapping_naver import NaverEconomyScraper


st.set_page_config(layout="wide")
load_dotenv()

# --- 사이드바 렌더링 (사용은 안 함) ---
render_sidebar()


st.title("📰 경제 뉴스 모아보기")

# --- 스크래퍼 인스턴스 생성 ---
hani_scraper = HaniEconomyScraper()
naver_scraper = NaverEconomyScraper(delay=0.7)

# --- 뉴스 스크랩 ---
hani_news = hani_scraper.scrape_v2(limit=20)
naver_news = naver_scraper.scrape_news(limit=20)

# --- 두 컬럼으로 나누기 ---
col1, col2 = st.columns([0.5, 0.5], gap="small")

# --- 카드 렌더링 함수 ---
def render_news_card(news):
    with st.container():
        st.markdown("""
            <style>
            .news-card {
                padding: 10px;
                border: 1px solid #e6e6e6;
                border-radius: 8px;
                margin-bottom: 20px;
                background-color: #fafafa;
                box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
                max-width: 300px;
            }
            .news-card h3 {
                font-size: 12px;
            }
            .fixed-image {
                width: 80%;
                height: 150px;
                object-fit: cover;
                border-radius: 8px;
                margin-bottom: 10px;
            }
            </style>
        """, unsafe_allow_html=True)

        st.markdown('<div class="news-card">', unsafe_allow_html=True)

        st.subheader(news["title"])

        if news["image"]:
            st.markdown(
                f'<img src="{news["image"]}" class="fixed-image">',
                unsafe_allow_html=True
            )
<<<<<<< HEAD
        if st.button("📊 기사 분석 보기", key=f"analyze_{news['link']}_{random.randint(10000,100000)}"):
=======

        if st.button("📊 기사 분석 보기", key=f"analyze_{news['link']}"):
>>>>>>> origin/feature/NEWS-007
            st.session_state["news_url"] = news['link']
            st.switch_page("pages/News_Analysis.py")

        pub = news.get('pub_date', '등록일 없음')
        update = news.get('update_date', None)

        if update:
            st.caption(f"🕓 등록일: {pub} / 수정일: {update}")
        else:
            st.caption(f"🕓 작성일: {pub}")

        st.markdown('</div>', unsafe_allow_html=True)

# --- 한겨레 뉴스 표시 ---
with col1:
    st.header("한겨레 경제 뉴스")
    if hani_news:
        for news in hani_news:
            render_news_card(news)
    else:
        st.write("🔎 한겨레 뉴스를 불러올 수 없습니다.")

# --- 네이버 뉴스 표시 ---
with col2:
    st.header("네이버 경제 뉴스")
    if naver_news:
        for news in naver_news:
            render_news_card(news)
    else:
        st.write("🔎 네이버 뉴스를 불러올 수 없습니다.")
