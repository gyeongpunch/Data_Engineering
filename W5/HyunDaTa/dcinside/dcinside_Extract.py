import yaml
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import pandas as pd
import re

# YAML 파일 읽기
with open('config.yaml', 'r', encoding='utf-8') as file:
    config = yaml.safe_load(file)

# URL 설정
base_url = config['Community']['dcinside']['domestic']

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
columns = ['Date', 'Title', 'Body', 'Comment']
df = pd.DataFrame(columns=columns)

keywords = ['정몽규', '축협']

try:
    for keyword in keywords:
        page = 1
        while True:
            # URL 설정
            if page == 1:
                search_url = f"https://gall.dcinside.com/board/lists/?id=football_k&s_type=search_subject_memo&s_keyword={keyword}"
            else:
                search_url = f"https://gall.dcinside.com/board/lists/?id=football_k&page={page}&search_pos=&s_type=search_subject_memo&s_keyword={keyword}"
            
            driver.get(search_url)
            
            # 검색 결과 페이지 로딩 대기
            time.sleep(1)
            
            # 페이지 소스 가져오기
            page_source = driver.page_source
            
            # BeautifulSoup으로 HTML 파싱
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # 글 목록 추출
            articles = soup.find_all('tr', {'class': 'ub-content us-post'})
            
            if not articles:
                break  # 더 이상 게시물이 없으면 루프 종료
            
            for article in articles:
                title_element = article.find('a', {'class': 'subject'})
                if title_element:
                    title = title_element.get_text(strip=True)
                    
                    # 본문 URL
                    post_url = "https://gall.dcinside.com" + title_element['href']
                    driver.get(post_url)
                    
                    # 본문 페이지 로딩 대기
                    time.sleep(0.2)
                    
                    # 본문 페이지 소스 가져오기
                    post_page_source = driver.page_source
                    post_soup = BeautifulSoup(post_page_source, 'html.parser')
                    
                    # 본문 내용 추출
                    body_content = post_soup.find('div', {'class': 'write_div'})
                    body_text = body_content.get_text(strip=True) if body_content else ''
                    
                    # 댓글 추출
                    comments_elements = post_soup.find_all('div', {'class': 'comment_txt'})
                    comments = [comment.get_text(strip=True) for comment in comments_elements]
                    comments_string = '\n'.join(comments)
                    
                    # 날짜와 시간 추출
                    date_time_element = post_soup.find('span', {'class': 'gall_date'})
                    date_time = date_time_element['title'] if date_time_element else ''
                    
                    # DataFrame에 행 추가
                    new_row = pd.DataFrame([{'Date': date_time, 'Title': title, 'Body': body_text, 'Comment': comments_string}])
                    df = pd.concat([df, new_row], ignore_index=True)
                    
                    print(f"Processed post: {title}")
                    print("-" * 50)
                    
                    # 목록 페이지로 다시 돌아가기
                    driver.back()
                    time.sleep(0.2)
            
            page += 1

finally:
    # 드라이버 종료
    driver.quit()

# DataFrame을 CSV 파일로 저장
df.to_csv('dcinside_extract.csv', index=False, encoding='utf-8-sig')
