import requests
from bs4 import BeautifulSoup
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager



class MailWebScrapping:
    def __init__(self):
        self.url = "https://www.mk.co.kr/news/economy/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
            "Referer": "https://www.mk.co.kr/news/economy/"
        }
        
    def scrape_news_v2(self,page=1):
        url = f"https://www.mk.co.kr/_CP/42?page={page}&lang=null&lcode=economy&scode=latest&date=null&category=null&mediaCode=null&sort=null&userNo=null&ga_category=data-category_1depth%3D%7C%EB%89%B4%EC%8A%A4%7C%20data-category_2depth%3D%7C%EA%B2%BD%EC%A0%9C%7C%20data-category_3depth%3D%7C%ED%99%88%7C%20%20data-section%3D%7C%EC%B5%9C%EC%8B%A0%EA%B8%B0%EC%82%AC%7C"
        ## 검색
        res = requests.get(url, headers=self.headers)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'html.parser')
        
        news_value = []
        
        news_list = soup.select("ul.latest_news_list > li")
        
        print (soup)
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
            
        return news_value  
    
    def scrape_all_page(self, page_range=1):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        

        all_news_list = []

        for page in range(1, page_range + 1):
            url = f"https://www.mk.co.kr/_CP/42?page={page}&lang=null&lcode=economy&scode=latest&date=null&category=null&mediaCode=null&sort=null&userNo=null&ga_category=data-category_1depth%3D%7C%EB%89%B4%EC%8A%A4%7C%20data-category_2depth%3D%7C%EA%B2%BD%EC%A0%9C%7C%20data-category_3depth%3D%7C%ED%99%88%7C%20%20data-section%3D%7C%EC%B5%9C%EC%8B%A0%EA%B8%B0%EC%82%AC%7C"
            driver.get(url)
            time.sleep(3)

            news_items = driver.find_elements(By.CSS_SELECTOR, "ul.latest_news_list > li")

            for item in news_items:
                class_attr = item.get_attribute("class")
                if class_attr and "ad_wrap" in class_attr:
                    continue

                try:
                    link_elem = item.find_element(By.CSS_SELECTOR, "a")
                    link = link_elem.get_attribute("href")

                    # 이미지
                    try:
                        image_elem = link_elem.find_element(By.CSS_SELECTOR, "div.thumb_area > img")
                        thumb = image_elem.get_attribute("src")
                    except:
                        thumb = "assets/image.png"

                    # 제목
                    title_elem = link_elem.find_element(By.CSS_SELECTOR, "div.txt_area > h3.news_ttl")
                    title = title_elem.text

                    # 발행일
                    pub_elem = link_elem.find_element(By.CSS_SELECTOR, "div.time_area > span")
                    pub_date = pub_elem.text

                    all_news_list.append({
                        "title": title,
                        "link": link,
                        "thumb": thumb,
                        "pub_date": pub_date
                    })

                except:
                    continue

        driver.quit()
        return all_news_list
            
            
            
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
        return news_list  
                    
                
   
        
if __name__ == "__main__":
    test = MailWebScrapping()
    test.scrape_news_v2(page=1)