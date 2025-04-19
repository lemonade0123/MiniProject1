import streamlit as st
import os
from dotenv import load_dotenv
from components.sidebar import render_sidebar
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

load_dotenv()

# --- 사이드바 렌더링 ---
render_sidebar()

st.title("🔥 한겨레 - 가장 많이 본 뉴스")

# --- 인기 기사 가져오기 ---
@st.cache_resource
def get_popular_articles():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.get("https://www.hani.co.kr/arti/economy")
    time.sleep(3)

    articles = driver.find_elements(By.CSS_SELECTOR, "a.ArticleAsideMostReadList_item__XtF8a")
    news_list = []

    for article in articles[:5]:
        title = article.find_element(By.CSS_SELECTOR, "span.ArticleAsideMostReadList_title__MZ22w").text
        link = article.get_attribute("href")
        news_list.append({
            "title": title,
            "link": link
        })

    driver.quit()
    return news_list

# --- 카드 스타일 뉴스 보여주기 (크기 줄인 버전) ---
def render_popular_card(news):
    with st.container():
        st.markdown("""<style>
            .news-card {
                padding: 8px 12px;
                border: 1px solid #e6e6e6
                border-radius: 1px;
                margin-bottom: 12px;
                background-color: #fffbe6;
                box-shadow: 1px 1px 3px rgba(0,0,0,0.05);
                max-width: 500px;
                font-size: 14px;
            }
            .news-title {
                font-size: 16px;
                font-weight: 600;
                margin-bottom: 4px;
            }
            </style>""", unsafe_allow_html=True)

        st.markdown('<div class="news-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="news-title">{news["title"]}</div>', unsafe_allow_html=True)
        st.markdown(f"[📰 기사 보기]({news['link']})", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# --- 인기 기사 렌더링 ---
def get_popular_page():
    with st.spinner("데이터를 불러오는 중입니다..."):
        popular_news = get_popular_articles()

    if popular_news:
        for article in popular_news:
            render_popular_card(article)
    else:
        st.warning("😥 인기 기사를 불러오지 못했습니다.")

