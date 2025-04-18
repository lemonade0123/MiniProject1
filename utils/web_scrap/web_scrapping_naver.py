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
        """네이버 경제 뉴스 스크래핑 (제목, 링크, 이미지, 상세 페이지에서 날짜 포함)"""
        res = requests.get(self.url, headers=self.headers)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'html.parser')

        articles = soup.select('ul.sa_list li')
        news_list = []

        for article in articles[:limit]:  # limit 개수만큼만
            title_tag = article.select_one('a.sa_text_title')
            img_tag = article.select_one('img')

            if title_tag:
                title = title_tag.get_text(strip=True)
                link = title_tag['href']

                # 이미지 src 또는 data-src
                image = None
                if img_tag:
                    image = img_tag.get('src') or img_tag.get('data-src')

                # 링크 들어가서 기사 상세페이지에서 날짜 크롤링
                pub_date = self.fetch_article_date(link)

                news_list.append({
                    'title': title,
                    'link': link,
                    'image': image,
                    'pub_date': pub_date
                })

                time.sleep(self.delay)

        return news_list

    def fetch_article_date(self, article_url):
        """기사 상세 페이지에 들어가서 작성 날짜 가져오기"""
        try:
            res = requests.get(article_url, headers=self.headers, timeout=5)
            res.encoding = 'utf-8'
            soup = BeautifulSoup(res.text, 'html.parser')

            date_tag = soup.select_one('span.media_end_head_info_datestamp_time._ARTICLE_DATE_TIME')
            if date_tag and date_tag.get('data-date-time'):
                return date_tag['data-date-time']
            return None
        except Exception as e:
            print(f"날짜 가져오기 실패: {e}")
            return None

    def get_news(self, news_url):
        
        res = requests.get(news_url, headers=self.headers, timeout=5)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'html.parser')
        
        news_div = soup.select_one("#ct")
        
        result = {}
        ## 제목 크롤링
        result["news_title"] = news_div.select_one("#title_area").text
        ## 날짜 크롤링
        result["news_publish_date"] = news_div.select_one("span.media_end_head_info_datestamp_time")["data-date-time"].split(" ")[0]
        
        ## 기사 내용 크롤링
        text = news_div.find('article', {'id': 'dic_area'})
        result["news_text"] = text.get_text(separator='\n', strip=True)
        
        return result
        
        
if __name__ == "__main__":
    print("Naver 경제 뉴스")

    scraper = NaverEconomyScraper(delay=0.7)  # 0.7초 딜레이 설정
    news_items = scraper.scrape_news(limit=5)

    if news_items:
        for news in news_items:
            print(f"- {news['title']}")
            print(f"  링크: {news['link']}")
            print(f"  이미지: {news['image']}")
            print(f"  날짜: {news['pub_date']}\n")
    else:
        print("뉴스 기사를 찾을 수 없습니다.")