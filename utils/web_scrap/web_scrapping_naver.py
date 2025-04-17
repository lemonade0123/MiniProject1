import requests
from bs4 import BeautifulSoup
import time

class NaverEconomyScraper:
    def __init__(self, delay=0.5):
        self.url = "https://news.naver.com/section/101"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
        }
        self.delay = delay  # 요청 간 딜레이 (초)

    def scrape_news(self, limit=5):
        """네이버 경제 뉴스 스크래핑"""
        res = requests.get(self.url, headers=self.headers)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'html.parser')

        articles = soup.select('ul.sa_list li')
        news_list = []

        for article in articles[:limit]:  # limit 개수만큼만 가져오기
            title_tag = article.select_one('a.sa_text_title')
            img_tag = article.select_one('img')

            if title_tag:
                title = title_tag.get_text(strip=True)
                link = title_tag['href']

                # 이미지 src 또는 data-src
                image = None
                if img_tag:
                    image = img_tag.get('src') or img_tag.get('data-src')

                news_list.append({
                    'title': title,
                    'link': link,
                    'image': image
                })

                # 요청 간 딜레이 추가
                time.sleep(self.delay)

        return news_list

## 테스트용용
# if __name__ == "__main__":
#     print("Naver 경제 뉴스")

#     scraper = NaverEconomyScraper(delay=0.7)
#     news_items = scraper.scrape_news(limit=5)

#     if news_items:
#         for news in news_items:
#             print(f"- {news['title']}")
#             print(f"  링크: {news['link']}")
#             print(f"  이미지: {news['image']}\n")
#     else:
#         print("뉴스 기사를 찾을 수 없습니다.")