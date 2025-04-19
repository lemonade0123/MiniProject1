import streamlit as st
import os
from dotenv import load_dotenv
from datetime import datetime, date

# --- 컴포넌트 및 스크래퍼 임포트 ---
from components.sidebar import render_sidebar
from utils.web_scrap.web_scrapping_han import HaniEconomyScraper
from utils.web_scrap.web_scrapping_naver import NaverEconomyScraper

st.set_page_config(layout="wide")
# --- 초기 설정 ---
load_dotenv()

# --- 사이드바 렌더링 (start, end, keyword 받아오기) ---
start_date, end_date, keyword = render_sidebar()

st.title("📰 경제 뉴스 모아보기")

# --- 스크래퍼 인스턴스 생성 ---
hani_scraper = HaniEconomyScraper()
naver_scraper = NaverEconomyScraper(delay=0.7)

# --- 뉴스 스크랩 ---
hani_news = hani_scraper.scrape_v2(limit=20)  # 한겨레도 최대 20개 스크랩하도록 수정
naver_news = naver_scraper.scrape_news(limit=20)  # 네이버도 최대 20개 스크랩

# --- 뉴스 필터링 함수 ---
def filter_news(news_list, start_date, end_date, keyword):
    filtered = []
    for news in news_list:
        pub_date_str = news.get('pub_date')

        pub_date = None
        if pub_date_str:
            try:
                pub_date = datetime.strptime(pub_date_str[:10], "%Y-%m-%d").date()
            except:
                pass

        matches_date = True
        if pub_date:
            matches_date = start_date <= pub_date <= end_date

        matches_keyword = keyword.lower() in news['title'].lower() if keyword else True

        if matches_date and matches_keyword:
            filtered.append(news)
    return filtered

# --- 필터링 적용 ---
filtered_hani_news = filter_news(hani_news, start_date, end_date, keyword)
filtered_naver_news = filter_news(naver_news, start_date, end_date, keyword)


# --- 두 컬럼으로 나누기 (가로폭 줄이기) ---
col1, col2 = st.columns([0.5, 0.5], gap="small")

# --- 카드 스타일 통일 함수 ---
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
                max-width: 300px;  # 카드 너비 조정
            }
            .news-card h3 {
                font-size: 12px;  # 제목 크기 조정
            }
            .fixed-image {
                width: 80%;
                height: 150px;
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
        if st.button("📊 기사 분석 보기", key=f"analyze_{news['link']}"):
            st.session_state["news_url"] = news['link']
            st.switch_page("pages/News_Analysis.py")
        # st.markdown(f"[📰 기사 전체 보기]({news['link']})", unsafe_allow_html=True)

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
    if filtered_hani_news:
        for news in filtered_hani_news[:20]:  # 최대 5개 보여주기 (필터링 결과에서)
            render_news_card(news)
    else:
        st.write("🔎 조건에 맞는 한겨레 뉴스를 찾을 수 없습니다.")

# --- 네이버 뉴스 표시 ---
with col2:
    st.header("네이버 경제 뉴스")
    if filtered_naver_news:
        for news in filtered_naver_news[:20]:  # 최대 5개 보여주기 (필터링 결과에서)
            render_news_card(news)
    else:
        st.write("🔎 조건에 맞는 네이버 뉴스를 찾을 수 없습니다.")

