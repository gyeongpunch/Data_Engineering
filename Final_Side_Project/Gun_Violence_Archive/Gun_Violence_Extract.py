import asyncio
import dateutil.parser as dateparser
import logging as log
import sys
import time
import pandas as pd
from argparse import ArgumentParser
from calendar import monthrange
from datetime import date, timedelta
from functools import partial
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from urllib.parse import parse_qs, urlparse

# 실행 example python3 Gun_Violence_Extract.py {start_Year-Month-Day} {end_Year-Month-Day} {Output_file}


# 날짜 format '%m/%d/%Y'로 설정
DATE_FORMAT = '%m/%d/%Y'

MESSAGE_NO_INCIDENTS_AVAILABLE = 'No Available Data'

def parse_args():
    targets_specific_month = False

    if len(sys.argv) > 1:
        parts = sys.argv[1].split('-')
        if len(parts) == 2:
            targets_specific_month = True
            del sys.argv[1]

    parser = ArgumentParser() # 입력 인수 초기화
    if not targets_specific_month:
        parser.add_argument(
            'start_date',
            metavar='START',
            help="set start date",
            action='store',
        )
        parser.add_argument(
            'end_date',
            metavar='END',
            help="set end date",
            action='store',
        )
        parser.add_argument(
            'output_file',
            metavar='OUTFILE',
            help="set output file",
            action='store',
        )

    parser.add_argument( # 디버그 옵션
        '-d', '--debug',
        help="show debug information",
        action='store_const',
        dest='log_level',
        const=log.DEBUG,
        default=log.WARNING,
    )

    args = parser.parse_args() # 입력 인수를 Parsing
    if targets_specific_month:
        month, year = map(int, parts)
        end_day = monthrange(year, month)[1]
        args.start_date = '{}-01-{}'.format(month, year)
        args.end_date = '{}-{}-{}'.format(month, end_day, year)
        args.output_file = 'stage1.{:02d}.{:04d}.csv'.format(month, year)
    return args

def wait_for_element(driver, by, value, timeout=5): #Driver elemnet가 나타날 때까지 wait
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        return element
    except Exception as e:
        log.error(f"Element with {by} = {value} not found. Exception: {e}")
        return None

def scroll_to_bottom(driver): # 스크롤 후 로딩 시간 대기
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(0.5)

# Table Extract
def extract_table_data(driver):
    table = wait_for_element(driver, By.CSS_SELECTOR, 'table.responsive')
    if table: # Extract the headers Except Operations
        header = [th.text for th in table.find_elements(By.TAG_NAME, 'th') if th.text != 'Operations']
        header += ['Incident Link', 'Source Link']
        
        # print(f"Headers: {header}") # Print Headers for Debugging

        # Extract Data
        rows = table.find_elements(By.TAG_NAME, 'tr')
        data = []
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, 'td')
            if cells:
                row_data = [cell.text for cell in cells[:-1]] # Extract Data Except Operations
                
                # Extract Links
                incident_link = cells[-1].find_element(By.LINK_TEXT, 'View Incident').get_attribute('href')
                source_link = cells[-1].find_element(By.LINK_TEXT, 'View Source').get_attribute('href') if cells[-1].find_elements(By.LINK_TEXT, 'View Source') else ''
                
                # Append Links to Row Data
                row_data.extend([incident_link, source_link])
                
                # Check Row Data Length == Header Length
                if len(row_data) == len(header):
                    data.append(row_data)
                    # print(f"Check Data : {row_data}")
                else:
                    log.error(f"Row length {len(row_data)} does not match header length {len(header)}. Skipping this row.")
                    log.error(f"Row data: {row_data}")
        
        # Return Headers and Data
        return header, data
    # If there is no table -> return empty list
    return [], []

def go_to_next_page(driver): # Next Page 이동
    next_button = wait_for_element(driver, By.LINK_TEXT, 'next ›', 3)
    if next_button:
        next_button.click()
        return True
    return False

def query(driver, start_date, end_date):
    print(f"Start Date : {start_date.strftime(DATE_FORMAT)}, End Date : {end_date.strftime(DATE_FORMAT)}")
    driver.get('http://www.gunviolencearchive.org/query')

    try:
        scroll_to_bottom(driver) # Web Page의 맨 아래로 스크롤

        # 'Add a rule' 열기
        filter_dropdown_trigger = wait_for_element(driver, By.CSS_SELECTOR, '.filter-dropdown-trigger')
        if filter_dropdown_trigger:
            filter_dropdown_trigger.click()
        else:
            raise Exception("There is no 'Add a rule' Button")
        
        # Date filter 클릭
        date_link = wait_for_element(driver, By.LINK_TEXT, 'Date')
        if date_link:
            date_link.click()
        else:
            raise Exception("There is no Date filter Button")
        
        # From, To Date 입력 필드 찾기
        input_date_from = wait_for_element(driver, By.CSS_SELECTOR, 'input.fancy.date-picker-single.form-text[id*="filter-field-date-from"]')
        input_date_to = wait_for_element(driver, By.CSS_SELECTOR, 'input.fancy.date-picker-single.form-text[id*="filter-field-date-to"]')

        # From, To Date 입력 필드 둘 다 발견해야지
        if input_date_from and input_date_to:
            # 날짜 설정 함수
            def set_date(input_field, date):
                # 입력 필드 클릭하여 달력 열기
                input_field.click()
                time.sleep(0.1)

                # 년도 선택
                year_select = wait_for_element(driver, By.XPATH, "//div[@class='daterangepicker dropdown-menu single opensright show-calendar' and contains(@style, 'display: block')]//select[@class='yearselect']")
                year_select.click()
                time.sleep(0.1)
                year_option = wait_for_element(driver, By.XPATH, f"//div[@class='daterangepicker dropdown-menu single opensright show-calendar' and contains(@style, 'display: block')]//select[@class='yearselect']/option[@value='{date.year}']")
                year_option.click()
                time.sleep(0.1)

                # 월 선택
                month_select = wait_for_element(driver, By.XPATH, "//div[@class='daterangepicker dropdown-menu single opensright show-calendar' and contains(@style, 'display: block')]//select[@class='monthselect']")
                month_select.click()
                time.sleep(0.1)
                month_option = wait_for_element(driver, By.XPATH, f"//div[@class='daterangepicker dropdown-menu single opensright show-calendar' and contains(@style, 'display: block')]//select[@class='monthselect']/option[@value='{date.month - 1}']")
                month_option.click()
                time.sleep(0.1)

                # 일 선택
                day_element = wait_for_element(driver, By.XPATH, f"//div[@class='daterangepicker dropdown-menu single opensright show-calendar' and contains(@style, 'display: block')]//td[@class='available' and text()='{date.day}']")
                day_element.click()
                time.sleep(0.1)

            # 'From' 날짜 설정
            set_date(input_date_from, start_date)
            # print(f"New value in 'From' field: {input_date_from.get_attribute('value')}")

            # 'To' 날짜 설정
            set_date(input_date_to, end_date)
            #  print(f"New value in 'To' field: {input_date_to.get_attribute('value')}")
        else:
            raise Exception("There is no Date input fields")
        
        # 쿼리 제출 'Search' 버튼 클릭
        form_submit = wait_for_element(driver, By.ID, 'edit-actions-execute')
        if form_submit:
            form_submit.click()
        else:
            raise Exception("There is no 'Search' Button")
        
        return driver.current_url, get_n_pages(driver)
    except Exception as e:
        log.error(f"Error during query execution: {e}")
        return driver.current_url, 0

def get_n_pages(driver):
    try:
        last_page = wait_for_element(driver, By.CSS_SELECTOR, 'a[title="Go to last page"]', timeout=1)
        if last_page:
            last_url = last_page.get_attribute('href')
            form_data = urlparse(last_url).query
            n_pages = int(parse_qs(form_data)['page'][0]) + 1
            return n_pages
        else:
            raise Exception("There is no 'Last Page'")
    except NoSuchElementException:
        tds = driver.find_elements(By.CSS_SELECTOR, '.responsive tbody tr td')
        if len(tds) == 1 and tds[0].text == MESSAGE_NO_INCIDENTS_AVAILABLE:
            return 0
        return 1

async def main():
    # 입력 인수 Parsing
    args = parse_args()
    log.basicConfig(level=args.log_level)

    # Driver Option Setting
    options = ChromeOptions()
    options.add_argument('--no-sandbox')
    # 제대로 동작하는지 확인하기 위한 Debugging(필요 시 주석 해제)
    # options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')

    # Proxy Setting
    proxy = "MY_PORXY_ADRESS" 
    options.add_argument(f'--proxy-server={proxy}')

    # Google Driver Setting
    driver_path = "chromedriver"
    service = ChromeService(executable_path=driver_path)
    driver = Chrome(service=service, options=options)

    # 하루마다의 데이터를 Extract
    step = timedelta(days=1)
    global_start, global_end = dateparser.parse(args.start_date), dateparser.parse(args.end_date)
    start, end = global_start, global_start + step - timedelta(days=1)

    all_data = pd.DataFrame()  # Initialize an empty DataFrame

    while start <= global_end:
        query_url, n_pages = query(driver, start, end)
        if n_pages > 0:
            current_page = 1
            while current_page <= n_pages:
                scroll_to_bottom(driver)
                headers, data = extract_table_data(driver)
                if not all_data.empty:
                    temp_df = pd.DataFrame(data, columns=headers)
                    all_data = pd.concat([all_data, temp_df], ignore_index=True)
                else:
                    all_data = pd.DataFrame(data, columns=headers)
                if not go_to_next_page(driver):
                    break
                current_page += 1
        start, end = end + timedelta(days=1), min(global_end, end + step)
    
    # Dataframe으로 저장
    if not all_data.empty:
        all_data.to_csv(args.output_file, index=False)
        print(f"Data saved to {args.output_file}")
    else:
        print("No data found.")
    
    driver.quit()  # Ensure the driver is properly closed

if __name__ == '__main__':
    loop = asyncio.new_event_loop()  # Use new_event_loop() to avoid DeprecationWarning
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()
