# hani_scraper.py 파일에 작성
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

            og_image = soup.find('meta', property='og:image')
            image_url = og_image['content'] if og_image and og_image.get('content') else None

            pub_date = "등록일 없음"
            update_date = "수정일 없음"

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
