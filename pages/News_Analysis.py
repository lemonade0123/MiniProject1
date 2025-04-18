import streamlit as st
from components.layout import render_layout
from utils.ai.sentence_alanyzer import SentenceAnalyzer
import re

class NewsAnalysis:
    def __init__(self):
        self.analyzer = SentenceAnalyzer()
        
    def news_analysis(self):
        
        news_url = st.session_state["news_url"]
        
        if self.is_valid_url(news_url):
            
            self.analyzer.analyze_sentiment(news_url)
        else:
            pass
        
    
    def get_content(self):
        pass
    

    def is_valid_url(self, url):
        url_regex = re.compile(
            r'^(https?://)'  # http:// or https://
            r'((([A-Z0-9](?:[A-Z0-9-]*[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain name
            r'((\d{1,3}\.){3}\d{1,3})|'  # or IPv4 address
            r'localhost))'  # or localhost
            r'(:\d+)?'  # optional port
            r'(/[-A-Z0-9+&@#/%=~_|$!]*[A-Z0-9+&@#/%=~_|$])?'  # optional path
            r'(\?[;&A-Za-z0-9%_\.=+-]*)?'  # optional query
            r'(#[-A-Z0-9_+&@#/%=~_|]*)?$',  # optional fragment
            re.IGNORECASE
        )
        return re.match(url_regex, url) is not None
        



render_layout("뉴스 분석", left_content)