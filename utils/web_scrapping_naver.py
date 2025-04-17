import requests
from bs4 import BeautifulSoup

# 1. Naver News 경제 섹션
def scrape_naver_news():
    url = "https://news.naver.com/section/101"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
    }
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    
    articles = soup.select('ul.sa_list li')
    news_list = []

    for article in articles:
        title_tag = article.select_one('a.sa_text_title')
        img_tag = article.select_one('img')

        if title_tag:
            title = title_tag.get_text(strip=True)
            link = title_tag['href']
            
            # 이미지 src 또는 data-src에서 가져오기
            image = None
            if img_tag:
                image = img_tag.get('src') or img_tag.get('data-src')

            news_list.append({
                'title': title,
                'link': link,
                'image': image
            })
    
    return news_list

# 실행
if __name__ == "__main__":
    print("Naver 경제 뉴스")
    for news in scrape_naver_news()[:5]:
        print(f"- {news['title']}")
        print(f"  링크: {news['link']}")
        print(f"  이미지: {news['image']}\n")