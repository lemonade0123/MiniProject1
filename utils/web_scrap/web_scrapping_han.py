import requests
from bs4 import BeautifulSoup
import time

class HaniEconomyScraper:
    def __init__(self):
        self.rss_url = "https://www.hani.co.kr/rss/economy/"
        self.base_url = "https://www.hani.co.kr"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

    def scrape(self, limit=20):
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
                'link': self.base_url + link,
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


    def get_news(self, news_url):
        ## renewal2023->article_text
        res = requests.get(news_url, headers=self.headers, timeout=5)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'html.parser')
        
        article_div = soup.select_one("#renewal2023")
        
        ## 내용 찾을 수 없을때
        
        
        result = {}
        ## 제목 크롤링
        result["news_title"] = soup.select_one('[class^="ArticleDetailView_title__"]').text
        ## 날짜 크롤링
        date_ul = soup.find("ul", class_=lambda c: c and "ArticleDetailView_dateList" in c)
        date_items = date_ul.find_all("li", class_=lambda c: c and "ArticleDetailView_dateListItem" in c)
        for li in date_items:   
            text = li.get_text(strip=True)
            span = li.find("span")
            if not span:
                continue
            if "수정" in text:
                result["news_update_date"] = span.get_text(strip=True)
            elif "등록" in text:
                result["news_publish_date"] = span.get_text(strip=True)
        
        
        ## 기사 내용 크롤링
        p_texts = soup.find_all("p", class_="text")
        ## 본문 크롤링
        result["news_text"] = "\n".join(p.get_text(strip=True) for p in p_texts[:-1])
        
        return result
        
        
    def scrape_v2(self, limit=20, page=1):

        url = "https://www.hani.co.kr/arti/economy/economy_general"
        if(page != 1):
            url = f'{url}?page={page}'
        ## 검색        
        res = requests.get(url, headers=self.headers)
        
        res.encoding = "utf-8"
        soup = BeautifulSoup(res.text, "html.parser")

        ## 데이터 넣기
        news_list = []

        ## 아이템 찾기
        search_news_list = soup.select("div[class^='section_left'] > div > ul > li[class^='ArticleList_item']")

        for news in search_news_list:
            # 이미지 찾기
            image = news.select_one("article > div[class^='BaseArticleCard_card'] a > div > div > div > img")["src"]

            # 링크 찾기
            link = news.select_one("article > div[class^='BaseArticleCard_card'] > div[class^='BaseArticleCard_content'] > a")["href"]

            # 제목 찾기
            title = news.select_one("article > div[class^='BaseArticleCard_card'] > div[class^='BaseArticleCard_content'] > a > div").getText()

            # 시간 찾기
            pub_date = news.select_one("article > div[class^='BaseArticleCard_card'] > div[class^='BaseArticleCard_content'] > div > div").getText()

            news_list.append({"title": title, "link": self.base_url + link, "image": image, "pub_date": pub_date})
        
        return news_list


    def scrap_all_page(self, page_range=2):
        news_list = []
        for i in range(1,page_range + 1):
            news_list.extend(self.scrape_v2(page=i))
        
        return news_list

        
        
if __name__ == "__main__":
    scraper = HaniEconomyScraper()
    print(scraper.get_news("https://www.hani.co.kr/arti/economy/economy_general/1193048.html"))