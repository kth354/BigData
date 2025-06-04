import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib

#CSV 파일 불러오기
station = pd.read_csv("지하철 혼잡도.csv", encoding='cp949')

#필요 없는 열 제거
station.drop(columns=['역번호', '상하구분'], inplace=True, errors='ignore')

#시간대 컬럼 추출
time_columns = station.columns[6:]  # '5시30분' ~ '00시30분'

#각 행마다 평균 혼잡도 계산
station['총혼잡도'] = station[time_columns].mean(axis=1)

#분석 대상 10개 주요 역 필터링
target_stations = ['강남', '홍대입구', '신도림', '고속터미널', '잠실',
                   '건대입구', '서울역', '동대문역사문화공원', '을지로입구', '신촌(지하)']
station = station[station['출발역'].isin(target_stations)]

#10개 역의 평균 혼잡도 계산
station_avg = station.groupby('출발역')['총혼잡도'].mean().sort_values()

#시각화
plt.figure(figsize=(10, 6))
plt.bar(station_avg.index, station_avg.values)
plt.title('주요 10개 역 평균 혼잡도 비교')
plt.xlabel('지하철역')
plt.ylabel('평균 혼잡도지수')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# 비혼잡 지하철역 TOP 5
#데이터 불러오기
station = pd.read_csv("지하철 혼잡도.csv", encoding='cp949')

#시간대 컬럼만 추출
time_columns = station.columns[6:]  # '5시30분' ~ '00시30분'

#평균 혼잡도 계산해서 새로운 열 추가
station['총혼잡도'] = station[time_columns].mean(axis=1)

#출발역별 평균 혼잡도 계산 후 낮은 순으로 정렬 → 상위 5개
top5_station_avg = station.groupby('출발역')['총혼잡도'].mean().sort_values().head(5)

#시각화
plt.figure(figsize=(8, 5))
plt.bar(top5_station_avg.index, top5_station_avg.values)
plt.title('비혼잡한 지하철역 TOP 5')
plt.xlabel('지하철역')
plt.ylabel('평균 혼잡도지수')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
