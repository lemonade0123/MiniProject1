import streamlit as st
import os
from dotenv import load_dotenv
from components.sidebar import render_sidebar

# 스크래퍼 클래스 임포트
from utils.web_scrap.web_scrapping_han import HaniEconomyScraper
from utils.web_scrap.web_scrapping_naver import NaverEconomyScraper

load_dotenv()
render_sidebar()

st.title("📰 경제 뉴스 모아보기")

# --- 스크래퍼 인스턴스 생성 ---
hani_scraper = HaniEconomyScraper()
naver_scraper = NaverEconomyScraper(delay=0.7)

# --- 뉴스 스크랩 ---
hani_news = hani_scraper.scrape()
naver_news = naver_scraper.scrape_news(limit=5)

# --- 두 컬럼으로 나누기 ---
col1, col2 = st.columns(2)

# --- 카드 스타일 통일 함수 ---
def render_news_card(news):
    with st.container():
        st.markdown(
            """
            <style>
            .news-card {
                padding: 10px;
                border: 1px solid #e6e6e6;
                border-radius: 8px;
                margin-bottom: 20px;
                background-color: #fafafa;
                box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
            }
            .fixed-image {
                width: 100%;
                height: 180px;
                object-fit: cover;
                border-radius: 8px;
                margin-bottom: 10px;
            }
            </style>
            """, unsafe_allow_html=True
        )

        st.markdown('<div class="news-card">', unsafe_allow_html=True)

        st.subheader(news["title"])

        if news["image"]:
            st.markdown(
                f'<img src="{news["image"]}" class="fixed-image">',
                unsafe_allow_html=True
            )

        st.markdown(f"[📰 기사 전체 보기]({news['link']})", unsafe_allow_html=True)

        # 등록일/수정일 모두 있으면 둘 다 표시
        pub = news.get('pub_date', '등록일 없음')
        update = news.get('update_date', None)

        if update:  # 수정일 있는 경우
            st.caption(f"🕓 등록일: {pub} / 수정일: {update}")
        else:  # 수정일 없는 경우
            st.caption(f"🕓 작성일: {pub}")

        st.markdown('</div>', unsafe_allow_html=True)

# --- 컬럼 나누기 (가운데 빈공간 늘리기) ---
col1, spacer, col2 = st.columns([5, 1, 5])  # 비율 (5 : 1 : 5)

# --- 한겨레 뉴스 표시 ---
with col1:
    st.header("한겨레 경제 뉴스")
    if hani_news:
        for news in hani_news[:5]:
            render_news_card(news)
    else:
        st.write("한겨레 뉴스를 가져오지 못했습니다.")

# --- 네이버 뉴스 표시 ---
with col2:
    st.header("네이버 경제 뉴스")
    if naver_news:
        for news in naver_news:
            render_news_card(news)
    else:
        st.write("네이버 뉴스를 가져오지 못했습니다.")
