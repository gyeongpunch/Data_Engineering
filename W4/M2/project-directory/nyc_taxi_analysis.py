import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp, hour, avg, count, unix_timestamp
import pandas as pd
import matplotlib.pyplot as plt

# Spark 세션 생성
spark = SparkSession.builder \
    .appName("NYC Taxi Analysis") \
    .master("local[*]") \
    .getOrCreate()

# Parquet 파일 로드
file_path = "data/yellow_tripdata_2024-01.parquet"
df = spark.read.parquet(file_path)

# 데이터 프레임 스키마 확인
df.printSchema()

# 누락된 값 제거
df = df.dropna()

# 시간 필드 변환
df = df.withColumn("pickup_datetime", to_timestamp(col("tpep_pickup_datetime")))\
       .withColumn("dropoff_datetime", to_timestamp(col("tpep_dropoff_datetime")))

# 비정상 값 필터링 (예: 음수 여행 시간, 음수 거리)
df = df.filter((col("trip_distance") > 0) & (col("tpep_dropoff_datetime") > col("tpep_pickup_datetime")))

# 여행 시간 계산 (unix_timestamp를 사용하여 에포크 시간으로 변환)
df = df.withColumn("trip_duration", (unix_timestamp(col("tpep_dropoff_datetime")) - unix_timestamp(col("tpep_pickup_datetime"))) / 60)

# 평균 여행 시간 계산
avg_trip_duration = df.agg(avg("trip_duration")).first()[0]

# 평균 여행 거리 계산
avg_trip_distance = df.agg(avg("trip_distance")).first()[0]

print(f"Average Trip Duration: {avg_trip_duration} minutes")
print(f"Average Trip Distance: {avg_trip_distance} miles")

# 시간대 추출
df = df.withColumn("hour", hour(col("pickup_datetime")))

# 시간대별 여행 수 계산
hourly_trips = df.groupBy("hour").agg(count("*").alias("trip_count")).orderBy("hour")

# 시간대별 여행 수 시각화
hourly_trips_pd = hourly_trips.toPandas()

plt.figure(figsize=(12, 6))
plt.bar(hourly_trips_pd["hour"], hourly_trips_pd["trip_count"])
plt.xlabel("Hour of the Day")
plt.ylabel("Number of Trips")
plt.title("Number of Trips per Hour of the Day")
plt.xticks(range(0, 24))
plt.grid(True)
plt.show()

# 결과 저장
output_path = "results/hourly_trips.csv"
hourly_trips_pd.to_csv(output_path, index=False)
