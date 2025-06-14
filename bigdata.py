import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 1. 데이터 불러오기
station = pd.read_csv("지하철 혼잡도.csv",  encoding='cp949')

# 2. 시간대 칼럼을 HH:MM 형식으로 영어로 변경
new_time_cols = {}
for col in station.columns:
    if '시' in col and '분' in col:
        hour = col.split('시')[0].zfill(2)
        minute = col.split('시')[1].replace('분', '').zfill(2)
        new_time_cols[col] = f"{hour}:{minute}"
station = station.rename(columns=new_time_cols)

# 3. 2호선 역만 필터링 (수동 리스트)
line2_stations = [
    '강남', '역삼', '선릉', '삼성', '종합운동장', '신천', '잠실', '잠실새내',
    '신정', '양천구청', '도림천', '신도림', '구로디지털단지', '건대입구', '홍대입구', '신촌'
]
station = station[station['출발역'].isin(line2_stations)]

# 4. 출발역 한글명을 영어로 매핑 (차트용)
station_name_map = {
    '강남': 'Gangnam',
    '역삼': 'Yeoksam',
    '선릉': 'Seolleung',
    '삼성': 'Samseong',
    '종합운동장': 'Sports Complex',
    '신천': 'Sincheon',
    '잠실': 'Jamsil',
    '잠실새내': 'Jamsilsaenae',
    '신정': 'Sinjeong',
    '양천구청': 'Yangcheon-gu Office',
    '도림천': 'Dorimcheon',
    '신도림': 'Sindorim',
    '구로디지털단지': 'Guro Digital Complex',
    '건대입구': 'Konkuk Univ.',
    '홍대입구': 'Hongdae',
    '신촌': 'Sinchon'
}
station['영문역명'] = station['출발역'].replace(station_name_map)

# 5. 시간대 컬럼 추출 (09:00~23:00 사이)
time_columns = [col for col in station.columns if ':' in col and '09:00' <= col <= '23:00']

# 6. 각 행에 대한 평균 혼잡도 계산
station['총혼잡도'] = station[time_columns].mean(axis=1)

# 7. 출발역별 평균 혼잡도 계산 후 상위 10개 역 추출
mean_congestion = station.groupby('출발역')['총혼잡도'].mean()
top10_station_names = mean_congestion.sort_values(ascending=False).head(10).index.tolist()

# 8. 상위 10개 역 데이터만 추출
top10_data = station[station['출발역'].isin(top10_station_names)]

# 9. 전치된 데이터프레임으로 시간대별 평균 혼잡도
pivot_df = top10_data.groupby('영문역명')[time_columns].mean().T

# 10. 시각화
plt.figure(figsize=(14, 7))
for 역이름 in pivot_df.columns:
    plt.plot(pivot_df.index, pivot_df[역이름], label=역이름, marker='o')

plt.title('Average Congestion by Time – Top 10 Stations on Line 2')
plt.xlabel('Time')
plt.ylabel('Congestion Index')
plt.xticks(rotation=45)
plt.legend(title='Station', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()


# ====== 혼잡도 낮은 역 TOP 5 ======

# 8. 혼잡도 평균 계산
station['총혼잡도'] = station[time_columns].mean(axis=1)

# 9. 평균 혼잡도가 낮은 역 5개 추출
least_crowded = (
    station.groupby('영문역명')['총혼잡도']
    .mean()
    .sort_values()
    .head(5)
    .index
)

# 10. 해당 역들만 필터링
top5_data = station[station['영문역명'].isin(least_crowded)]

# 11. 시간대별 평균 혼잡도 재계산
pivot_df = top5_data.groupby('영문역명')[time_columns].mean().T

# 12. 시각화 (비혼잡 역)
plt.figure(figsize=(14, 7))
for 역이름 in pivot_df.columns:
    plt.plot(pivot_df.index, pivot_df[역이름], label=역이름, marker='o')

plt.title('Least Crowded 5 Stations – Avg Congestion by Time')
plt.xlabel('Time')
plt.ylabel('Congestion Index')
plt.xticks(rotation=45)
plt.legend(title='Station', fontsize=9, bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()
