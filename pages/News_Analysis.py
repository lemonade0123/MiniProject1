import streamlit as st
from components.layout import render_layout
from utils.ai.sentence_alanyzer import SentenceAnalyzer
from utils.web_scrap.web_scrapping_han import HaniEconomyScraper
from utils.web_scrap.web_scrapping_naver import NaverEconomyScraper
from utils.tokenizer.tokenizer import tokenizer
from urllib.parse import urlparse
from components.sidebar import render_sidebar
from utils.graph.graph_visualizer import GraphVisualizer
import re


class NewsAnalysis:
    def __init__(self):
        self.analyzer = SentenceAnalyzer()
        self.tokenizer = tokenizer()
        self.haniEconomyScraper = HaniEconomyScraper()
        self.naverEconomyScraper = NaverEconomyScraper()
        self.graphVisualizer = GraphVisualizer()

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
        news_url = st.session_state["news_url"]
        print(news_url)
        if self.is_valid_url(news_url):
            
            ## 뉴스를 가져오기
            news_info = self.get_news_info(news_url)
            
             # 타이틀, 날짜 출력
            st.markdown(f"## 💡 {news_info["news_title"]}")
            st.markdown(f"##### 🕑출판일 : {news_info["news_publish_date"]}")
            
            
            left_col, right_col, whitespace = st.columns((9, 7, 1))

            ## 단어 가져오기
            keywords = self.tokenizer.top_keywords_count(news_info["news_text"], count=20)
            
            
            with left_col:
                ## 단어 시각화
                if len(keywords) == 0 :
                    st.warning("데이터가 비어 있어요. 먼저 데이터를 확인해주세요.")
                else:
                    
                    st.markdown(f"## 🔑 키워드 ")
                    fig = self.graphVisualizer.generate_wordcloud_figure(keywords)
                    st.pyplot(fig)  
                    
                    # keyword_df = self.graphVisualizer.generate_dataframe(sorted(keywords, key=lambda x: x[1], reverse=True)[:5], ["키워드","등장 수"])
                    # styled_table = keyword_df.to_html(index=False)
                    # styled_html = f"""
                    # <div style="font-size: 20px;">
                    #     {styled_table}
                    # </div>
                    # """

                    # st.markdown(styled_html, unsafe_allow_html=True)
            
                    
            with right_col:

                st.markdown(f"## 🔗 URL ")
                st.markdown(f"#### {news_url}")
                st.markdown("<br>", unsafe_allow_html=True)  # 두 줄 띄우기
                
                sentiment_result = ""
                sentiment_data = self.analyzer.analyze_sentiment(news_info["news_text"])
                if(sentiment_data["부정"] < sentiment_data["긍정"]):
                    sentiment_result = f"😀 긍정 : {format(sentiment_data["긍정"], '.2f')}"
                else:
                    sentiment_result = f"😢 부정 : {format(sentiment_data["부정"], '.2f')} "
                    
                
                st.markdown(f"## 📝 감성분석 결과:  {sentiment_result}")
                st.markdown("<br>", unsafe_allow_html=True)  # 두 줄 띄우기
                    
                # sentiment_fig = self.graphVisualizer.generate_pychart_figure(title="감성분석", data=sentiment_data)
                # st.pyplot(sentiment_fig)  
                ## 요약
                summation = self.analyzer.summarize(news_info["news_text"])
                # 요약본
                st.markdown(f"## 💬 요약 ")
                st.markdown(f'#### {summation}')
                

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



render_sidebar()
render_layout("📰 뉴스 분석", NewsAnalysis().get_content)
