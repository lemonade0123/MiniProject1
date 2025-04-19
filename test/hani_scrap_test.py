from bs4 import BeautifulSoup
import requests


url = "https://www.mk.co.kr/search?word=%ED%8A%B8%EB%9F%BC%ED%94%84"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.mk.co.kr/news/economy/",
}

res = requests.get(url, headers=headers)
res.encoding = 'utf-8'
soup = BeautifulSoup(res.text, 'html.parser')


file_name = "scraped_page.html"  # 저장할 파일 이름 설정
with open(file_name, "w", encoding="utf-8") as f:
    f.write(soup.prettify()) 