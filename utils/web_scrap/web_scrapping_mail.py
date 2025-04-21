import requests
from bs4 import BeautifulSoup
import time

class MailWebScrapping:
    def __init__(self):
        self.url = "https://www.mk.co.kr/news/economy/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://www.mk.co.kr/news/economy/",
        }
        
    def scrape_news(self, search_keyword=""):
        url = self.url
        
        if(search_keyword != ""):
            url += f"search?word={search_keyword}&sort=desc&dateType=all&searchField=all&newsType=all"
        
        
        ## 검색
        res = requests.get(url, headers=self.headers)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'html.parser')
        
        
        ## 값 넣기
        
        news_value = []
        if(search_keyword != ""):
            # news_list = soup.select("")
            
            file_name = "scraped_page.html"  # 저장할 파일 이름 설정
            with open(file_name, "w", encoding="utf-8") as f:
                f.write(soup.prettify()) 
            print(soup)
        else:
            news_list = soup.select("ul.latest_news_list > li")

        for news in news_list: 
            if "ad_wrap" in news.get("class", []):
                continue
            
            ## 이미지, 시간, 제목, 링크
            try:
                link = news.select_one("a")["href"]
                image_url = news.select_one("a > div.thumb_area > img")
                thumb = image_url.get("src") if image_url else "assets/image.png"
                
                title = news.select_one("a > div.txt_area > h3.news_ttl").text
                pub_date = news.select_one("a > div.time_area > span").text
            
                news_value.append({
                    "title": title,
                    "link" : link,
                    "thumb" : thumb,
                    "pub_date" : pub_date
                })
                
            except:
                continue
                    
                    
                
   
        
if __name__ == "__main__":
    test = MailWebScrapping()
    test.scrape_news("트럼프")