import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout,
    QLineEdit, QListWidget, QMessageBox
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class SubwayApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Subway Congestion Viewer - Line 2 Only")
        self.setGeometry(100, 100, 1000, 800)  # ✅ GUI 기본 크기 넉넉히 설정

        self.init_data()   # ✅ 데이터 불러오기 및 전처리
        self.init_ui()     # ✅ UI 초기화

    def init_data(self):
        # ✅ 1. CSV 불러오기
        df = pd.read_csv("지하철 혼잡도.csv", encoding='cp949')

        # ✅ 2. 열 이름 표준화
        df = df.rename(columns={'호선': 'Line', '출발역': 'Station'})

        # ✅ 3. 시간대 컬럼 영어 형식으로 변경 (HH:MM)
        new_time_cols = {}
        for col in df.columns:
            if '시' in col and '분' in col:
                hour = col.split('시')[0].zfill(2)
                minute = col.split('시')[1].replace('분', '').zfill(2)
                new_time_cols[col] = f"{hour}:{minute}"
        df = df.rename(columns=new_time_cols)

        # ✅ 4. 시간대 컬럼만 필터링 (09:00~23:00)
        self.time_cols = [col for col in df.columns if ':' in col and '09:00' <= col <= '23:00']

        # ✅ 5. 2호선만 필터링
        df = df[df['Line'].astype(str).str.contains('2')]

        # ✅ 6. 2호선 전체 영어 매핑 (누락된 역 추가)
        name_map = {
            '강남': 'Gangnam', '역삼': 'Yeoksam', '선릉': 'Seolleung', '삼성': 'Samseong',
            '종합운동장': 'Sports Complex', '신천': 'Sincheon', '잠실': 'Jamsil',
            '잠실새내': 'Jamsilsaenae', '신정': 'Sinjeong', '양천구청': 'Yangcheon-gu Office',
            '도림천': 'Dorimcheon', '신도림': 'Sindorim', '구로디지털단지': 'Guro Digital Complex',
            '건대입구': 'Konkuk Univ.', '홍대입구': 'Hongdae', '신촌': 'Sinchon',
            '서울대입구': 'Seoul Natl Univ.', '뚝섬': 'Ttukseom', '성수': 'Seongsu',
            '왕십리': 'Wangsimni', '낙성대': 'Nakseongdae', '사당': 'Sadang',
            '방배': 'Bangbae', '서초': 'Seocho', '교대': 'Gyodae',
            '을지로입구': 'Euljiro 1-ga', '을지로3가': 'Euljiro 3-ga',
            '충정로': 'Chungjeongno', '동대문역사문화공원': 'Dongdaemun H&C Park',
            '강변': 'Gangbyeon', '구의': 'Guui', '까치산': 'Kkachisan', '당산': 'Dangsan',
            '대림': 'Daerim', '봉천': 'Bongcheon', '시청': 'City Hall', '신답': 'Sindap',
            '신당': 'Sindang', '신대방': 'Sindaebang', '신림': 'Sillim', '신설동': 'Sinseol-dong',
            '신정네거리': 'Sinjeongnegeori', '아현': 'Ahyeon', '영등포구청': 'Yeongdeungpo-gu Office',
            '용답': 'Yongdap', '용두': 'Yongdu', '이대': 'Ewha Womans Univ.',
            '잠실나루': 'Jamsilnaru', '한양대': 'Hanyang Univ.', '합정': 'Hapjeong',
            '문래': 'Mullae', '상왕십리': 'Sangwangsimni', '신촌(지하)': 'Sinchon (Underground)', '을지로4가': 'Euljiro 4-ga'
        }

        df['영문역명'] = df['Station'].map(name_map).fillna(df['Station'])

        # ✅ 7. numpy로 평균 혼잡도 계산
        df['총혼잡도'] = np.mean(df[self.time_cols].values, axis=1)

        # ✅ 8. 필요한 변수 저장
        self.df = df
        self.station_names = sorted(df['영문역명'].unique())

    def init_ui(self):
        layout = QVBoxLayout()

        # ✅ 검색창
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search station (e.g., Gangnam)")
        self.search_bar.textChanged.connect(self.filter_list)
        layout.addWidget(self.search_bar)

        # ✅ 역 리스트
        self.list_widget = QListWidget()
        self.list_widget.addItems(self.station_names)
        layout.addWidget(self.list_widget)

        # ✅ 버튼
        self.btn_plot = QPushButton("Plot Congestion")
        self.btn_plot.clicked.connect(self.draw_plot)
        layout.addWidget(self.btn_plot)

        # ✅ 그래프 캔버스
        self.figure = Figure(figsize=(12, 6))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.setLayout(layout)

    def filter_list(self, text):
        self.list_widget.clear()
        filtered = [name for name in self.station_names if text.lower() in name.lower()]
        self.list_widget.addItems(filtered)

    def draw_plot(self):
        selected = self.list_widget.currentItem()
        if not selected:
            QMessageBox.warning(self, "No selection", "Please select a station.")
            return

        station_name = selected.text()
        df_filtered = self.df[self.df['영문역명'] == station_name]
        pivot = df_filtered.groupby('영문역명')[self.time_cols].mean().T

        # ✅ 그래프 그리기
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(pivot.index, pivot[station_name], marker='o')
        ax.set_title(f"Congestion Trend – {station_name}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Congestion Index")
        ax.grid(True, linestyle='--', alpha=0.5)
        plt.setp(ax.get_xticklabels(), rotation=45)  # ✅ 시간 라벨 회전
        self.figure.tight_layout()
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SubwayApp()
    window.show()
    sys.exit(app.exec_())
