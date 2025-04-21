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
class KeywordVisualization:
    def __init__(self,font_path='C:\\Windows\\Fonts\\malgunsl.ttf'):
        self.db = get_db()
        self.font_path = font_path
        
        # 폰트 설정
        self.font_prop = fm.FontProperties(fname=self.font_path).get_name()
        plt.rcParams['font.family'] = self.font_prop

    def visualize_heatmap(self, df):
        """히트맵을 생성하는 함수"""
        
        df['append_count'] = df['append_count'].astype(int)
        
        pivot_df = df.pivot_table(index='append_date', columns='append_word', values='append_count', fill_value=0)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.heatmap(pivot_df,annot=False, fmt='1f', cmap='YlOrBr')
        plt.title('일별 키워드 등장 히트맵')
        plt.ylabel('날짜')
        plt.xlabel('키워드')
        plt.tight_layout()
        st.pyplot(fig)  # Streamlit에서 시각화 결과 출력

    def bar_chart(self, df, date):
        """날짜별 키워드 등장 횟수 바 차트"""
        
        df['append_count'] = df['append_count'].astype(int)
        
        day_df = df[df['append_date'] == date].sort_values(by='append_count', ascending=False)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(data=day_df, x='append_word', y='append_count', palette='viridis')
        plt.title(f"{date} 키워드 등장 횟수")
        plt.xlabel("키워드")
        plt.ylabel("등장 횟수")
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig)  # Streamlit에서 시각화 결과 출력
    
    def line_chart(self, df, keyword):
        """키워드 일별 등장 추이 라인 차트"""
        
        df['append_count'] = df['append_count'].astype(int)
        
        keyword_df = df[df['append_word'] == keyword]
        
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.lineplot(data=keyword_df, x='append_date', y='append_count', marker='o')
        plt.title(f'"{keyword}" 키워드 일별 등장 추이')
        plt.xlabel("날짜")
        plt.ylabel("등장 횟수")
        plt.grid(True)
        plt.tight_layout()
        st.pyplot(fig)  # Streamlit에서 시각화 결과 출력
    
    def generate_wordcloud_last_week(self):
        """최근 일주일 간의 워드클라우드 생성"""
        end_date = datetime.today()
        start_date = end_date - timedelta(days=6)
        
        start_str = start_date.strftime('%Y-%m-%d')
        end_str = end_date.strftime('%Y-%m-%d')

        # SQL 쿼리 실행
        sql = f"""
            SELECT append_word, SUM(append_count) AS total_count
            FROM word_list
            WHERE append_date BETWEEN '{start_str}' AND '{end_str}'
            GROUP BY append_word;
        """
        
        df = self.db.fetch_df(sql)
        
        if df.empty:
            st.write("최근 일주일 간 데이터가 없습니다.")
            return

        # 워드클라우드 생성
        word_freq = dict(zip(df['append_word'], [int(x) for x in df['total_count']]))
        
        
        wc = WordCloud(font_path=self.font_path, width=800, height=400, background_color='white')
        wc.generate_from_frequencies(word_freq)

        # 시각화
        fig, ax = plt.subplots(figsize=(12, 6))
        plt.imshow(wc, interpolation='bilinear')
        plt.axis('off')
        plt.title(f"{start_str} ~ {end_str} 워드클라우드")
        plt.tight_layout()
        st.pyplot(fig)  
        
