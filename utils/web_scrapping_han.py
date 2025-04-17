import requests
from bs4 import BeautifulSoup

def scrape_hani_economy_rss_with_image():
    rss_url = "https://www.hani.co.kr/rss/economy/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    res = requests.get(rss_url, headers=headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'xml')

    news_list = []

    items = soup.find_all('item')

    for item in items:
        title = item.title.get_text(strip=True)
        link = item.link.get_text(strip=True)

        # 대표 이미지 가져오기
        image_url = fetch_article_image(link, headers)

        news_list.append({
            'title': title,
            'link': link,
            'image': image_url
        })

    return news_list

def fetch_article_image(article_url, headers):
    try:
        res = requests.get(article_url, headers=headers, timeout=5)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'html.parser')

        # 대표 이미지 찾기 (기사 상단에 있는 이미지)
        og_image = soup.find('meta', property='og:image')
        if og_image and og_image.get('content'):
            return og_image['content']
        
        # og:image 없으면 대체 이미지 (또는 None)
        return None
    except Exception as e:
        print(f"이미지 가져오기 실패: {e}")
        return None

# 실행
if __name__ == "__main__":
    print("한겨레 경제 뉴스 (RSS + 이미지)")
    news_items = scrape_hani_economy_rss_with_image()
    if news_items:
        for news in news_items[:10]:  # 5개만 출력
            print(f"- {news['title']}")
            print(f"  링크: {news['link']}")
            print(f"  이미지: {news['image']}\n")
    else:
        print("뉴스 기사를 찾을 수 없습니다.")
