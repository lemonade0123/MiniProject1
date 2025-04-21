'''
테스트 케이스
스크랩 후 토큰화화 처리.
이후 데이터베이스에 insert 처리리

'''
# scrap_test.py 최상단에 아래 코드 추가
import sys
import os

# 루트 디렉토리 경로 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.web_scrap.web_scrapping_han import HanEconomyScraper
from utils.tokenizer.tokenizer import tokenizer
from utils.database.db_config import get_db
from collections import Counter



'''
1. Web Scraping
'''
scraper = HanEconomyScraper(delay=0.7)  # 0.7초 딜레이 설정
news_items = scraper.scrape_news(limit=5)



'''
2. word Tokenizing
'''
word_tokenizer = tokenizer()
word_raw_list = []
if news_items:
    for news in news_items:
        word_raw_list.extend(word_tokenizer.extract_keywords(news['title'])) 
else:
    print("뉴스 기사를 찾을 수 없습니다.")
    

'''
3. data preprocessing
수집한 데이터를 DB에 넣기 위해 집계 필요.
'''
aggregate_word_list =dict(Counter(word_raw_list))


date = "2025-04-21"  # 임시 날짜
append_word_list = [{"append_date": date, "append_word": word, "append_count": count} for word, count in aggregate_word_list.items()]

   
# '''
# 4. Insert Database
# '''

table_name = "word_list"
# TODO 지금은 강제로 넣지만 web scraping 날짜 개선하면 list 가 아닌 list[dict] 로 받을 예정
db = get_db()


db.insert(table_name,append_word_list)
    
    