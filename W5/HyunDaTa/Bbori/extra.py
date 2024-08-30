import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# 크롬 드라이버 설정
chrome_options = Options()
chrome_options.add_argument("--headless")  # 헤드리스 모드로 실행
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
service = Service('/Users/admin/Desktop/Data_Engineering/chromedriver')  # 크롬 드라이버 경로 설정
driver = webdriver.Chrome(service=service, options=chrome_options)

base_url = "https://gall.dcinside.com/board/lists/"
board_id = "maplestory_new"
search_pos = -6145874
search_keyword = ".EB.BF.8C.EB.A6.AC"

def get_post_details(post_url):
    try:
        driver.get(post_url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        title_tag = soup.find('span', class_='title_subject')
        title = title_tag.text.strip() if title_tag else 'No title'
        
        date_time_tag = soup.find('span', class_='gall_date')
        date_time = date_time_tag['title'] if date_time_tag else 'No date_time'
        
        body_div = soup.find('div', class_='write_div')
        body = body_div.get_text(strip=True) if body_div else "No content"
        
        comments = []
        comment_list = soup.find('ul', class_='cmt_list')
        if comment_list:
            comment_items = comment_list.find_all('li', class_='ub-content')
            for comment_item in comment_items:
                comment_text_tag = comment_item.find('div', class_='clear cmt_txtbox')
                comment_date_tag = comment_item.find('span', class_='date_time')
                if comment_text_tag and comment_date_tag:
                    comment_text = comment_text_tag.get_text(strip=True)
                    comment_date = comment_date_tag.text.strip()
                    comments.append(f"{comment_date}: {comment_text}")
        
        comments_str = ' | '.join(comments) if comments else pd.NA

        return {
            'title': title,
            'date_time': date_time,
            'body': body,
            'comments': comments_str
        }
    except Exception as e:
        print(f"Error fetching post details for URL {post_url}: {e}")
        return None

def fetch_posts_for_search_pos(search_pos, start_page, end_page):
    data = []

    for page in range(start_page, end_page + 1):
        print(f"Fetching page {page} with search_pos {search_pos}...")
        driver.get(f"{base_url}?id={board_id}&page={page}&search_pos={search_pos}&s_type=search_subject_memo&s_keyword={search_keyword}")
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        post_links = soup.select('tr.ub-content > td.gall_tit > a')
        
        if not post_links:
            print(f"No posts found on page {page}")
        
        for post_link in post_links:
            href = post_link['href']
            if href.startswith('/board/view/?id=maplestory_new'):
                post_url = "https://gall.dcinside.com" + href
                print(f"Fetching details for post: {post_url}")
                post_details = get_post_details(post_url)
                if post_details:
                    data.append(post_details)
                time.sleep(0.1)  # 웹사이트에 부담을 주지 않기 위해 대기 시간 추가

    return data

# 기존 데이터 불러오기
try:
    existing_df = pd.read_csv('Bboori.csv', encoding='utf-8-sig')
except FileNotFoundError:
    existing_df = pd.DataFrame()

# 새로운 데이터 가져오기 (16페이지부터 26페이지까지)
new_data = fetch_posts_for_search_pos(search_pos, 16, 26)

if new_data:
    new_df = pd.DataFrame(new_data)
    combined_df = pd.concat([existing_df, new_df], ignore_index=True)
    combined_df.to_csv('Bboori.csv', index=False, encoding='utf-8-sig')
    print("Data successfully saved to Bboori.csv")
else:
    print("No new data to save")

driver.quit()
