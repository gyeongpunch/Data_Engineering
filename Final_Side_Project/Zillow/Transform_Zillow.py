import pandas as pd
import googlemaps
from time import sleep

# 파일 경로 설정
file_path = 'Extract_Zillow_Result.csv'

# CSV 파일 읽기
df = pd.read_csv(file_path)

# Google Maps 클라이언트 초기화
api_key = 'AIzaSyDxwPoduMLwARN9G4J91rr9UhHPKOid9rc'  # 여기에 Google API 키를 입력하세요
gmaps = googlemaps.Client(key=api_key)

# 경도와 위도를 저장할 리스트 초기화
latitudes = []
longitudes = []

# 주소를 기반으로 경도와 위도 찾기
for address in df['address']:
    try:
        geocode_result = gmaps.geocode(address)
        if geocode_result:
            location = geocode_result[0]['geometry']['location']
            latitudes.append(location['lat'])
            longitudes.append(location['lng'])
        else:
            latitudes.append(None)
            longitudes.append(None)
        sleep(0.2)
    except Exception as e:
        latitudes.append(None)
        longitudes.append(None)

# 결과를 데이터프레임에 추가
df['latitude'] = latitudes
df['longitude'] = longitudes

# 데이터프레임 출력 (optional)
print(df.head())

# 결과 저장
output_path = 'Transform_Zillow_Result.csv'
df.to_csv(output_path, index=False)
print(f"Geocoded data saved to {output_path}")
