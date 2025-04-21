# scrap_test.py 최상단에 아래 코드 추가
import sys
import os

# 루트 디렉토리 경로 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.web_scrap.web_scrapping_han import HaniEconomyScraper
from utils.tokenizer.tokenizer import tokenizer
from utils.database.db_config import get_db
from collections import Counter


HaniEconomyScraper().scrap_all_page()


