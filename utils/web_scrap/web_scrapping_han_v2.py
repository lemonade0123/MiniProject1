import requests
from bs4 import BeautifulSoup
import time
import re


class HaniEconomyScraper:
    def __init__(self):
        self.news_url = "https://www.hani.co.kr/arti/economy/economy_general"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    def get_news(self, news_url):
        ## renewal2023->article_text
        res = requests.get(news_url, headers=self.headers, timeout=5)
        res.encoding = "utf-8"
        soup = BeautifulSoup(res.text, "html.parser")

        article_div = soup.select_one("#renewal2023")

        ## 내용 찾을 수 없을때

        result = {}
        ## 제목 크롤링
        result["news_title"] = soup.select_one(
            '[class^="ArticleDetailView_title__"]'
        ).text
        ## 날짜 크롤링
        date_ul = soup.find(
            "ul", class_=lambda c: c and "ArticleDetailView_dateList" in c
        )
        date_items = date_ul.find_all(
            "li", class_=lambda c: c and "ArticleDetailView_dateListItem" in c
        )
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

    def get_news_list(self, search_keyword="", start_date="", end_date=""):
        news_list = []

        ## 검색이 있을 때 url 변경이 필요함함
        ## url = https://search.hani.co.kr/search?searchword={search_keyword}sort=desc&startdate={start_date}&enddate={end_date}
        search_url = self.news_url

        if search_keyword != "":
            search_url = f"https://search.hani.co.kr/search?searchword={search_keyword}sort=desc"
            if(start_date != ""):
                search_url += f"startdate={start_date}"
            if(end_date != ""):
                search_url += f"enddate={end_date}"
        
        search_url += "&startdate=1988.01.01&enddate=2025.04.18&dt=all"

        ## 검색
        res = requests.get(search_url, headers=self.headers)
        res.encoding = "utf-8"
        soup = BeautifulSoup(res.text, "html.parser")

        file_name = "scraped_page.html"  # 저장할 파일 이름 설정
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(soup.prettify())  # 또는 f.write(html_content) 로 원본 HTML 저장 가

        ## 데이터 넣기
        news_list = []

        ## 검색이 아닐 시
        if search_keyword.__eq__(""):
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

                news_list.append({"title": title, "link": link, "image": image, "pub_date": pub_date})
                
        else:
            search_news_list = soup.select("div.search-result-section > ul.article-list > li")
            for news in search_news_list:
                 # 이미지 찾기
                image = re.search(r"url\((['\"]?)(?P<url>.+?)\1\)", news.select_one("article > a > div.thubnail")["style"])

                # 링크 찾기
                link = news.select_one("article > a >")["href"]
                
                # 날짜
                pub_date = news.select_one("article > a > div.article-list-cont > span.article-date ").getText()
            
                # 제목
                title = news.select_one("article > a > div.article-list-cont > strong").getText()
                
                
                news_list.append({"title": title, "link": link, "image": image, "pub_date": pub_date})
        
        print (news_list)
        return news_list

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
    scraper.get_news_list(search_keyword="테스트")
