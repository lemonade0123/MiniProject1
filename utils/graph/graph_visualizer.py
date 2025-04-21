import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm
from wordcloud import WordCloud
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# scrap_test.py 최상단에 아래 코드 추가
import sys
import os

# 루트 디렉토리 경로 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from utils.database.db_config import get_db

load_dotenv()


# 시각화 함수
class GraphVisualizer:
    def __init__(self,font_path='C:\\Windows\\Fonts\\malgunsl.ttf'):
        self.db = get_db()
        self.font_path = font_path
        
        # 폰트 설정
        self.font_prop = fm.FontProperties(fname=self.font_path).get_name()
        plt.rcParams['font.family'] = self.font_prop

    def generate_dataframe(self, keywords, headers):
        if isinstance(keywords, dict):
            data = list(keywords.items())
        elif isinstance(keywords, list):
            data = keywords    
        
            # 인덱스를 1부터 시작하도록 설정
        df = pd.DataFrame(data, columns=headers, index=range(1, len(data) + 1))
        return df
    
    def generate_wordcloud_figure(self, keywords):
        
        wc = WordCloud(font_path=self.font_path, width=700, height=400, background_color='white')
        
        if not isinstance(keywords, dict):
            try:
                keywords = dict(keywords)  # 예: list of tuples → dict로 변환
            except (ValueError, TypeError) as e:
                st.error("dict 또는 (key, value) 리스트 형태여야 합니다.")
                return
            
        wc.generate_from_frequencies(keywords)

        # 시각화
        fig, ax = plt.subplots(figsize=(12, 6))
        plt.imshow(wc, interpolation='bilinear')
        plt.axis('off')
        return fig
        
