import requests
from bs4 import BeautifulSoup
import time

class HaniEconomyScraper:
    def __init__(self):
        self.rss_url = "https://www.hani.co.kr/rss/economy/"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

    def scrape(self):
        res = requests.get(self.rss_url, headers=self.headers)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'xml')

        news_list = []
        items = soup.find_all('item')

        for item in items:
            title = item.title.get_text(strip=True)
            link = item.link.get_text(strip=True)

            image_url, pub_date, update_date = self.fetch_article_info(link)

            news_list.append({
                'title': title,
                'link': link,
                'image': image_url,
                'pub_date': pub_date,
                'update_date': update_date
            })

            time.sleep(0.5)

        return news_list

    def fetch_article_info(self, article_url):
        try:
            res = requests.get(article_url, headers=self.headers, timeout=5)
            res.encoding = 'utf-8'
            soup = BeautifulSoup(res.text, 'html.parser')

            # og:image 가져오기
            og_image = soup.find('meta', property='og:image')
            image_url = og_image['content'] if og_image and og_image.get('content') else None

            # 등록일/수정일 추출
            pub_date = "등록일 없음"
            update_date = "수정일 없음"

            # li 전체 탐색: "등록", "수정" 텍스트 기반 탐지
            li_tags = soup.find_all('li')
            for li in li_tags:
                li_text = li.get_text(strip=True)
                span = li.find('span')
                if not span:
                    continue
                date_text = span.get_text(strip=True)

                if "등록" in li_text:
                    pub_date = date_text
                elif "수정" in li_text:
                    update_date = date_text

            return image_url, pub_date, update_date

        except Exception as e:
            print(f"[오류] 기사 정보 가져오기 실패: {e}")
            return None, "등록일 없음", "수정일 없음"

    def display_news(self, news_list, limit=10):
        print("한겨레 경제 뉴스")
        if not news_list:
            print("뉴스 기사를 찾을 수 없습니다.")
            return

        for news in news_list[:limit]:
            print(f"- {news['title']}")
            print(f"  링크: {news['link']}")
            print(f"  이미지: {news['image']}")
            print(f"  등록일: {news['pub_date']}")
            print(f"  수정일: {news['update_date']}\n")

if __name__ == "__main__":
    scraper = HaniEconomyScraper()
    news_items = scraper.scrape()
    scraper.display_news(news_items)