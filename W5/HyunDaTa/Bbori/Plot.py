import pandas as pd
import matplotlib.pyplot as plt

# CSV 파일에서 데이터 읽기
df = pd.read_csv('Bboori.csv', encoding='utf-8-sig')

# 'date_time' 열을 datetime 형식으로 변환, 올바르지 않은 값은 NaT로 변환
df['date_time'] = pd.to_datetime(df['date_time'], format='%Y-%m-%d %H:%M:%S', errors='coerce')

# NaT 값을 제외
df = df.dropna(subset=['date_time'])

# 'date' 열 추가 (연-월-일)
df['date'] = df['date_time'].dt.date

# 일별 게시물 개수 집계 및 누적합 계산
daily_counts = df.groupby('date').size().cumsum()

# 선 그래프 그리기
plt.figure(figsize=(12, 6))
plt.plot(daily_counts.index, daily_counts.values, marker='o', linestyle='-')

# 그래프 제목과 축 레이블 설정
plt.title('Cumulative Number of Posts per Day')
plt.xlabel('Date')
plt.ylabel('Cumulative Number of Posts')

# x축 레이블 설정: 매일 표시
plt.xticks(pd.date_range(start=daily_counts.index.min(), end=daily_counts.index.max(), freq='D'), rotation=45)

plt.grid(True)
plt.tight_layout()
plt.show()
