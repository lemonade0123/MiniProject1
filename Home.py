import streamlit as st
import os
from dotenv import load_dotenv
from datetime import date

# --- 컴포넌트 및 스크래퍼 임포트 ---
from components.sidebar import render_sidebar
from components.layout import render_layout
from utils.web_scrap.web_scrapping_han import HaniEconomyScraper
from utils.web_scrap.web_scrapping_naver import NaverEconomyScraper

load_dotenv()

# --- 페이지 설정 ---
st.set_page_config(layout="wide")

# --- 사이드바 렌더링 ---
start_date, end_date, keyword = render_sidebar()


class HomePage:

    def __init__(self):
        pass

    def render_news_card(self, news):
        with st.container():
            st.markdown("""
                <style>
                .news-card {
                    padding: 8px;
                    border: 1px solid #e6e6e6;
                    border-radius: 1px;
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


            st.subheader(news["title"])

            if news["image"]:
                st.markdown(
                    f'<img src="{news["image"]}" class="fixed-image">', unsafe_allow_html=True
                )
            if st.button("📊 기사 분석 보기", key=f"analyze_{news['link']}"):
                st.session_state['news_url'] = news['link']
                st.switch_page("pages/News_Analysis.py")

            pub = news.get('pub_date', '등록일 없음')
            update = news.get('update_date', None)

            if update:
                st.caption(f"🕓 등록일: {pub} / 수정일: {update}")
            else:
                st.caption(f"🕓 작성일: {pub}")


    def home_page(self):
        # --- 스크래퍼 인스턴스 생성 ---
        hani_scraper = HaniEconomyScraper()
        naver_scraper = NaverEconomyScraper(delay=0.7)

        # --- 뉴스 스크랩 ---
        hani_news = hani_scraper.scrape_v2(limit=20)
        naver_news = naver_scraper.scrape_news(limit=20)

        # --- 필터링 함수 ---
        def filter_news(news_list):
            filtered = []
            for news in news_list:
                pub_date = news.get("pub_date", "")
                if pub_date:
                    try:
                        pub_date_obj = date.fromisoformat(pub_date[:10])
                    except:
                        continue
                    if not (start_date <= pub_date_obj <= end_date):
                        continue
                if keyword:
                    if keyword.lower() not in news["title"].lower() and keyword.lower() not in news.get("content", "").lower():
                        continue
                filtered.append(news)
            return filtered

        hani_news = filter_news(hani_news)
        naver_news = filter_news(naver_news)

        # --- 두 컬럼으로 나누기 ---
        col1, col2 = st.columns([0.5, 0.5], gap="small")

        # --- 한겨레 뉴스 표시 ---
        with col1:
            st.header("한겨레 경제 뉴스")
            st.markdown('<hr style="border: 1px solid #ccc;">', unsafe_allow_html=True)
            if hani_news:
                for news in hani_news:
                    self.render_news_card(news)
            else:
                st.write("🔎 조건에 맞는 한겨레 뉴스가 없습니다.")

        # --- 네이버 뉴스 표시 ---
        with col2:
            st.header("네이버 경제 뉴스")
            st.markdown('<hr style="border: 1px solid #ccc;">', unsafe_allow_html=True)
            if naver_news:
                for news in naver_news:
                    self.render_news_card(news)
            else:
                st.write("🔎 조건에 맞는 네이버 뉴스가 없습니다.")


# --- 메인 렌더링 실행 ---
render_layout("📰 경제 뉴스 모아보기", left_func=HomePage().home_page)