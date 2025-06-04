import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

station = pd.read_csv("지하철 혼잡도.csv", encoding='cp949')
station.drop(columns=['역번호', '상하구분'], inplace=True, errors='ignore')
target_stations = ['강남', '홍대입구', '신도림', '고속터미널', '잠실',
                   '건대입구', '서울역', '동대문역사문화공원', '을지로입구', '신촌']
station = station[station['출발역'].isin(target_stations)]
print(station)