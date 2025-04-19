import streamlit as st
from components.layout import render_layout
from utils.ai.sentence_alanyzer import SentenceAnalyzer
from utils.web_scrap.web_scrapping_han import HaniEconomyScraper
from utils.web_scrap.web_scrapping_naver import NaverEconomyScraper
from utils.tokenizer.tokenizer import tokenizer
from urllib.parse import urlparse
from components.sidebar import render_sidebar
import re


class NewsAnalysis:
    def __init__(self):
        self.analyzer = SentenceAnalyzer()
        self.tokenizer = tokenizer()
        self.haniEconomyScraper = HaniEconomyScraper()
        self.naverEconomyScraper = NaverEconomyScraper()

    def news_analysis(self):
        # 한겨레, 네이버뉴스 나누어야함.

        news_url = st.session_state["news_url"]

        if self.is_valid_url(news_url):
            self.analyzer.analyze_sentiment(news_url)
        else:
            pass

    """
    {
        news_title: 제목,
        news_update_date : 업데이트 날짜,
        news_publish_date : 출판 날짜,
        news_text : 본문문
    }
    """

    def get_content(self):
        ## 원본. 밑에는 테스트용 값 박기
        # news_url = st.session_state["news_url"]
        news_url = "https://www.hani.co.kr/arti/economy/economy_general/1193192.html"
        if self.is_valid_url(news_url):
            ## 뉴스를 가져오기
            news_info = self.get_news_info(news_url)
            ## 가져온 뉴스를 분석하기
            ## 단어 가져오기
            keywords = self.tokenizer.top_five_keywords(news_info["news_text"])
            ## 요약
            summation = self.analyzer.summarize(news_info["news_text"])
            ## 분석한 내용을 토대로 뿌려주기
            # 타이틀, 날짜 출력
            st.markdown(f"## {news_info["news_title"]}")
            st.markdown(f"### {news_info["news_publish_date"]}")
            # 단어 리스트
            st.markdown(f"**키워드** {", ".join(keywords)}")
            # 요약본
            st.markdown(f"요약 : {summation}")

        else:
            st.markdown("## 조회되지 않는 url 입니다.")

    def is_valid_url(self, url):
        url_regex = re.compile(
            r"^(https?://)"  # http:// or https://
            r"((([A-Z0-9](?:[A-Z0-9-]*[A-Z0-9])?\.)+(?:[A-Z]{2,6}|[A-Z0-9-]{2,})|"  # domain name
            r"((\d{1,3}\.){3}\d{1,3})|"  # or IPv4 address
            r"localhost))"  # or localhost
            r"(:\d+)?"  # optional port
            r"(/[-A-Z0-9+&@#/%=~_|$!.]*)*"  # <-- path 부분 수정
            r"(\?[;&A-Za-z0-9%_\.=+-]*)?"  # optional query
            r"(#[-A-Z0-9_+&@#/%=~_|]*)?$",  # optional fragment
            re.IGNORECASE,
        )
        return re.match(url_regex, url) is not None

    def get_news_info(self, url):
        parsed = urlparse(url)
        domain = parsed.netloc
        path = parsed.path

        if "hani.co.kr" in domain:
            return self.haniEconomyScraper.get_news(url)

        elif "naver.com" in domain:
            return self.naverEconomyScraper.get_news(url)



st.set_page_config(layout="wide")
render_sidebar()
render_layout("📰 뉴스 분석", NewsAnalysis().get_content)
