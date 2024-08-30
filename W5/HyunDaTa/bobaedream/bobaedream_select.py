import sqlite3
import pandas as pd

# SQLite 데이터베이스에 연결
conn = sqlite3.connect('bobaedream.db')

# SQL 쿼리 작성
query = '''
SELECT * FROM bobaedream_load_result
WHERE Title LIKE '%아이오닉%' OR Title LIKE '%누수%'
   OR Body LIKE '%아이오닉%' OR Body LIKE '%누수%'
'''

# 쿼리 실행 및 결과를 데이터프레임으로 변환
df_result = pd.read_sql_query(query, conn)

# 데이터베이스 연결 종료
conn.close()

# 결과 출력
print(df_result)
