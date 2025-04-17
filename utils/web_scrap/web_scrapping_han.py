import requests
from bs4 import BeautifulSoup
import time  

class HanEconomyScraper:
    def __init__(self, delay=0.5):
        self.rss_url = "https://www.hani.co.kr/rss/economy/"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        self.delay = delay  # 요청 간 딜레이 (초)

    def scrape_news(self, limit=5):
        """한겨레 경제 뉴스 스크래핑"""
        res = requests.get(self.rss_url, headers=self.headers)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'xml')

        news_list = []
        items = soup.find_all('item')

        for item in items[:limit]:  # limit 수 만큼만 가져오기
            title = item.title.get_text(strip=True)
            link = item.link.get_text(strip=True)

            # 요청 간 딜레이 추가
            time.sleep(self.delay)
            image_url = self._fetch_article_image(link)

            news_list.append({
                'title': title,
                'link': link,
                'image': image_url
            })

        return news_list

    def _fetch_article_image(self, article_url):
        """기사 본문에서 대표 이미지 추출"""
        try:
            res = requests.get(article_url, headers=self.headers, timeout=5)
            res.encoding = 'utf-8'
            soup = BeautifulSoup(res.text, 'html.parser')

            og_image = soup.find('meta', property='og:image')
            if og_image and og_image.get('content'):
                return og_image['content']

            return None
        except Exception as e:
            print(f"이미지 가져오기 실패: {e}")
            return None


## 테스트용
# if __name__ == "__main__":
#     print("한겨레 경제 뉴스")

#     scraper = HaniEconomyScraper(delay=0.7)  # 0.7초 딜레이 설정
#     news_items = scraper.scrape_news(limit=5)

#     if news_items:
#         for news in news_items:
#             print(f"- {news['title']}")
#             print(f"  링크: {news['link']}")
#             print(f"  이미지: {news['image']}\n")
#     else:
#         print("뉴스 기사를 찾을 수 없습니다.")
