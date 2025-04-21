from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# 크롬 옵션 설정
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# 크롬 드라이버 자동 설치
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# 웹사이트 접속
driver.get("https://www.hani.co.kr/arti/economy")
time.sleep(3)

# 기사 추출 (많이 본 뉴스 영역)
articles = driver.find_elements(By.CSS_SELECTOR, "a.ArticleAsideMostReadList_item__XtF8a")

# 최대 5개까지만 출력
for i, article in enumerate(articles[:5], 1):
    title = article.find_element(By.CSS_SELECTOR, "span.ArticleAsideMostReadList_title__MZ22w").text
    link = article.get_attribute("href")
    print(f"[{i}] {title}\n링크: {link}\n")

driver.quit()
