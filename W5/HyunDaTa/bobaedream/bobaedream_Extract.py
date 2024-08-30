import yaml
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import pandas as pd
import re

# Config 파일 읽기
with open('bobaedream_config.yaml', 'r', encoding='utf-8') as file:
    config = yaml.safe_load(file)

# URL 설정
base_url = config['Community']['bobaedream']['free']
keywords = config['Keyword']['ioniq6']

# 크롬 드라이버 경로 설정
chrome_driver_path = "/Users/admin/Desktop/Data_Engineering/chromedriver"

# 크롬 옵션 설정
chrome_options = Options()
chrome_options.add_argument("--headless")  # 헤드리스 모드
chrome_options.add_argument("--disable-gpu")  # GPU 비활성화 (일부 시스템에서는 필요)
chrome_options.add_argument("--window-size=1920x1080")  # 화면 크기 설정
chrome_options.add_argument("--no-sandbox")  # 샌드박스 비활성화 (리눅스에서 필요할 수 있음)
chrome_options.add_argument("--disable-dev-shm-usage")  # /dev/shm 사용 비활성화 (리눅스에서 필요할 수 있음)

# 드라이버 설정
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# DataFrame 초기화
columns = ['Date', 'Time', 'Title', 'Body', 'Comment']
df = pd.DataFrame(columns=columns)

def extract_articles_from_page(page_source):
    global df
    soup = BeautifulSoup(page_source, 'html.parser')
    articles = soup.find_all('tr', {'itemscope': '', 'itemtype': 'http://schema.org/Article'})
    
    if not articles:
        return False  # 더 이상 게시물이 없음을 의미
    
    for article in articles:
        title_element = article.find('a', {'class': 'bsubject'})
        if title_element:
            title = title_element.get_text(strip=True)
            post_url = "https://www.bobaedream.co.kr" + title_element['href']
            driver.get(post_url)
            time.sleep(0.2)
            post_page_source = driver.page_source
            post_soup = BeautifulSoup(post_page_source, 'html.parser')
            body_content = post_soup.find('div', {'class': 'bodyCont'})
            body_text = body_content.get_text(strip=True) if body_content else ''
            date_time_element = post_soup.find('span', {'class': 'countGroup'})
            if date_time_element:
                date_time_text = date_time_element.get_text(strip=True)
                date_time_match = re.search(r'(\d{4}\.\d{2}\.\d{2})\s*\(\w+\)\s*(\d{2}:\d{2})', date_time_text)
                if date_time_match:
                    date = date_time_match.group(1)
                    time_of_day = date_time_match.group(2)
                else:
                    date = ''
                    time_of_day = ''
            else:
                date = ''
                time_of_day = ''
            comments = post_soup.find_all('dd', {'id': lambda x: x and x.startswith('small_cmt_')})
            comment_texts = [comment.get_text(strip=True) for comment in comments]
            comments_string = '\n'.join(comment_texts)
            new_row = pd.DataFrame([{'Date': date, 'Time': time_of_day, 'Title': title, 'Body': body_text, 'Comment': comments_string}])
            df = pd.concat([df, new_row], ignore_index=True)
            print(f"Processed post: {title}")
            print("-" * 50)
            driver.back()
            time.sleep(0.2)
    return True

try:
    for keyword in keywords:
        current_page = 1
        while True:
            search_url = f"{base_url}&s_select=Body&s_key={keyword}&page={current_page}"
            driver.get(search_url)
            time.sleep(1)
            page_source = driver.page_source
            has_articles = extract_articles_from_page(page_source)
            
            if not has_articles:
                break  # 더 이상 게시물이 없으면 크롤링 종료

            current_page += 1

finally:
    driver.quit()

df.to_csv('bobaedream_Extract_Result.csv', index=False, encoding='utf-8-sig')
