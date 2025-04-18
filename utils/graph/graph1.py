import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm
from wordcloud import WordCloud
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

# Database 연결 클래스
class Database:
    def __init__(self):
        self.engine = create_engine(
            os.getenv("DATABASE_URL"),
            pool_size=5,
            max_overflow=2,
            pool_recycle=1800,
            pool_pre_ping=True
        )

    def fetch_df(self, query: str, params: dict = None):
        with self.engine.connect() as conn:
            result = conn.execute(text(query), params or {})
            df = pd.DataFrame(result.fetchall(), columns=result.keys())
            return df

    def execute(self, query: str, params: dict = None):
        with self.engine.connect() as conn:
            conn.execute(text(query), params or {})
            conn.commit()

    def insert(self, table_name: str, data: dict):
        if isinstance(data, dict):
            data = [data]  # 단일 row도 리스트로 변환

        if not data:
            return  # 빈 리스트면 아무 것도 하지 않음

        columns = ', '.join(data[0].keys())
        placeholders = ', '.join([f":{key}" for key in data[0].keys()])
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        with self.engine.connect() as conn:
            conn.execute(text(query), data)  # 리스트 넘기면 다건 처리됨
            conn.commit()

# 연결 재사용을 위한 캐싱 처리
@st.cache_resource
def get_db():
    return Database()


# 시각화 함수
class KeywordVisualization:
    def __init__(self, db: Database, font_path='C:\\Windows\\Fonts\\malgunsl.ttf'):
        self.db = db
        self.font_path = font_path
        
        # 폰트 설정
        self.font_prop = fm.FontProperties(fname=self.font_path).get_name()
        plt.rcParams['font.family'] = self.font_prop

    def visualize_heatmap(self, df):
        """히트맵을 생성하는 함수"""
        pivot_df = df.pivot_table(index='append_date', columns='append_word', values='append_count', fill_value=0)
        
        plt.figure(figsize=(14, 8))
        sns.heatmap(pivot_df, annot=True, fmt='d', cmap='YlOrBr')
        plt.title('일별 키워드 등장 히트맵')
        plt.ylabel('날짜')
        plt.xlabel('키워드')
        plt.tight_layout()
        st.pyplot()  # Streamlit에서 시각화 결과 출력

    def bar_chart(self, df, date):
        """날짜별 키워드 등장 횟수 바 차트"""
        day_df = df[df['append_date'] == date].sort_values(by='append_count', ascending=False)
        
        plt.figure(figsize=(10, 6))
        sns.barplot(data=day_df, x='append_word', y='append_count', palette='viridis')
        plt.title(f"{date} 키워드 등장 횟수")
        plt.xlabel("키워드")
        plt.ylabel("등장 횟수")
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot()  # Streamlit에서 시각화 결과 출력
    
    def line_chart(self, df, keyword):
        """키워드 일별 등장 추이 라인 차트"""
        keyword_df = df[df['append_word'] == keyword]
        
        plt.figure(figsize=(10, 5))
        sns.lineplot(data=keyword_df, x='append_date', y='append_count', marker='o')
        plt.title(f'"{keyword}" 키워드 일별 등장 추이')
        plt.xlabel("날짜")
        plt.ylabel("등장 횟수")
        plt.grid(True)
        plt.tight_layout()
        st.pyplot()  # Streamlit에서 시각화 결과 출력
    
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
        word_freq = dict(zip(df['append_word'], df['total_count']))
        wc = WordCloud(font_path=self.font_path, width=800, height=400, background_color='white')
        wc.generate_from_frequencies(word_freq)

        # 시각화
        plt.figure(figsize=(12, 6))
        plt.imshow(wc, interpolation='bilinear')
        plt.axis('off')
        plt.title(f"{start_str} ~ {end_str} 워드클라우드")
        st.pyplot()  