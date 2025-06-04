import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib  # 설치된 경우에만

# 1. 데이터 불러오기
station = pd.read_csv("지하철 혼잡도.csv", encoding='cp949')

# 2. 10개 주요 역만 필터링
target_stations = ['강남', '홍대입구', '신도림', '고속터미널', '잠실',
                   '건대입구', '서울역', '동대문역사문화공원', '을지로입구', '신촌']
station = station[station['출발역'].isin(target_stations)]

# 3. 시간대 컬럼 추출
time_columns = station.columns[6:]  # '5시30분' ~ '00시30분'

# 4. 지하철역별 시간대 평균 혼잡도 계산
pivot_df = station.groupby('출발역')[time_columns].mean().T  # 전치해서 시간 기준으로

# 5. 시각화
plt.figure(figsize=(14, 7))

for 역이름 in pivot_df.columns:
    plt.plot(pivot_df.index, pivot_df[역이름], label=역이름, marker='o')

plt.title('10개 주요역의 시간대별 평균 혼잡도')
plt.xlabel('시간대')
plt.ylabel('혼잡도지수')
plt.xticks(rotation=45)
plt.legend(title='지하철역')
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()


# 1. CSV 파일 불러오기
station = pd.read_csv("지하철 혼잡도.csv", encoding='cp949')

# 2. 시간대 컬럼 추출
time_columns = station.columns[6:]  # '5시30분' ~ '00시30분'

# 3. 총혼잡도 열 생성 (시간대 평균)
station['총혼잡도'] = station[time_columns].mean(axis=1)

# 4. 출발역별 평균 혼잡도 계산 → 낮은 순 → 상위 5개 역 이름 추출
top5_station_names = (
    station.groupby('출발역')['총혼잡도']
    .mean()
    .sort_values()
    .head(5)
    .index
)

# 5. 해당 5개 역 데이터만 추출
top5_data = station[station['출발역'].isin(top5_station_names)]

# 6. 지하철역별 시간대별 평균 혼잡도 계산
pivot_df = top5_data.groupby('출발역')[time_columns].mean().T

# 7. 시각화
plt.figure(figsize=(14, 7))

for 역이름 in pivot_df.columns:
    plt.plot(pivot_df.index, pivot_df[역이름], label=역이름, marker='o')

plt.title('비혼잡한 지하철역 TOP 5의 시간대별 평균 혼잡도')
plt.xlabel('시간대')
plt.ylabel('평균 혼잡도지수')
plt.xticks(rotation=45)
plt.legend(title='지하철역')
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()
