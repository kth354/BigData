import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib

#데이터 불러오기
station = pd.read_csv("지하철 혼잡도.csv", encoding='cp949')

#시간대 컬럼 추출
time_columns = station.columns[6:]  # '5시30분' ~ '00시30분'

#사용자에게 역 이름 입력 받기
역이름 = input("혼잡도 시각화를 원하는 지하철역 이름을 입력하세요: ")

#해당 역 데이터 필터링
역_데이터 = station[station['출발역'] == 역이름]

#예외 처리: 없는 역 입력한 경우
if 역_데이터.empty:
    print(f"'{역이름}' 역은 데이터에 없습니다. 다시 확인해주세요.")
else:
    #시간대별 평균 혼잡도 계산
    시간대별_혼잡도 = 역_데이터[time_columns].mean()

    #시각화
    plt.figure(figsize=(12, 6))
    plt.plot(시간대별_혼잡도.index, 시간대별_혼잡도.values, marker='o')
    plt.title(f"{역이름} 시간대별 평균 혼잡도")
    plt.xlabel('시간대')
    plt.ylabel('혼잡도지수')
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()
