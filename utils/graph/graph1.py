import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
import mysql.connector

# MySQL 연결
conn = mysql.connector.connect(
    host='your_host',          # MySQL 서버 호스트
    user='your_user',          # MySQL 사용자
    password='your_password',  # MySQL 비밀번호
    database='news_db'         # 사용할 데이터베이스
)

# SQL 쿼리 실행
query = "SELECT * FROM word_list"
df = pd.read_sql(query, conn)


for font in fm.fontManager.ttflist:
  print((font.name, font.fname))
[ (font.name, font.fname) for font in fm.fontManager.ttflist if 'Mal' in font.name ]

font_path = 'C:\\Windows\\Fonts\\malgunsl.ttf'
font_prop = fm.FontProperties(fname=font_path).get_name()

matplotlib.rc('font', family=font_prop)

df = pd.read_csv('weekly_keywords.csv')

def visualize_heatmap(df):
    pivot_df = df.pivot_table(index='append_date', columns='append_word', values='append_count', fill_value=0)

    plt.figure(figsize=(14, 8))
    sns.heatmap(pivot_df, annot=True, fmt='d', cmap='YlOrBr')
    plt.title('일별 키워드 등장 히트맵')
    plt.ylabel('날짜')
    plt.xlabel('키워드')
    plt.tight_layout()
    plt.show()
    
import seaborn as sns
import matplotlib.pyplot as plt

def bar_chart(df, date):
    day_df = df[df['append_date'] == date].sort_values(by='append_count', ascending=False)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(data=day_df, x='append_word', y='append_count', palette='viridis')
    plt.title(f"{date} 키워드 등장 횟수")
    plt.xlabel("키워드")
    plt.ylabel("등장 횟수")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    
def line_chart(df, keyword):
    keyword_df = df[df['append_word'] == keyword]
    
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=keyword_df, x='append_date', y='append_count', marker='o')
    plt.title(f'"{keyword}" 키워드 일별 등장 추이')
    plt.xlabel("날짜")
    plt.ylabel("등장 횟수")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    
    