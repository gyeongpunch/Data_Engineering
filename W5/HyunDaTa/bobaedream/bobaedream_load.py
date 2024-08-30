import pandas as pd
import sqlite3

# CSV 파일 읽기
df = pd.read_csv('bobaedream_Extract_Result.csv')

# post_id 컬럼 추가 (1부터 시작하여 각 행마다 고유 ID 부여)
df.insert(0, 'post_id', range(1, len(df) + 1))

# SQLite 데이터베이스에 연결 (파일이 없으면 자동으로 생성됨)
conn = sqlite3.connect('bobaedream.db')

# 데이터베이스 커서 생성
cursor = conn.cursor()

# 테이블 생성 (이미 존재하면 삭제 후 재생성)
cursor.execute('''
DROP TABLE IF EXISTS bobaedream_data
''')

cursor.execute('''
CREATE TABLE bobaedream_data (
    post_id INTEGER PRIMARY KEY,
    Date TEXT,
    Time TEXT,
    Title TEXT,
    Body TEXT,
    Comment TEXT
)
''')

# 데이터프레임을 SQLite 데이터베이스에 저장
df.to_sql('bobaedream_load_Result', conn, if_exists='append', index=False)

# 데이터베이스 연결 종료
conn.close()

print("Data has been successfully stored in the SQLite database with post_id as the primary key.")
