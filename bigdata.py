import sys
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib

from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QFileDialog,
    QCheckBox, QHBoxLayout, QMessageBox, QScrollArea
)

# pip install pyqt5 pandas matplotlib koreanize-matplotlib 라이브러리 설치 필요

class SubwayCongestionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("지하철 혼잡도 시각화 (PyQt5)")
        self.setGeometry(100, 100, 500, 600)

        self.file_path = None
        self.station_checkboxes = {}

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # CSV 불러오기 버튼
        self.load_button = QPushButton("CSV 파일 불러오기")
        self.load_button.clicked.connect(self.load_csv)
        layout.addWidget(self.load_button)

        layout.addWidget(QLabel("분석할 역을 선택하세요:"))

        # 역 선택 체크박스 (스크롤 가능)
        station_names = ['강남', '홍대입구', '신도림', '고속터미널', '잠실',
                         '건대입구', '서울역', '동대문역사문화공원', '을지로입구', '신촌']

        checkbox_layout = QVBoxLayout()
        for station in station_names:
            checkbox = QCheckBox(station)
            self.station_checkboxes[station] = checkbox
            checkbox_layout.addWidget(checkbox)

        scroll_widget = QWidget()
        scroll_widget.setLayout(checkbox_layout)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)

        # 버튼: 선그래프, 막대그래프
        button_layout = QHBoxLayout()
        self.line_btn = QPushButton("선그래프 시각화")
        self.line_btn.clicked.connect(self.draw_line_chart)
        button_layout.addWidget(self.line_btn)

        self.bar_btn = QPushButton("막대그래프 시각화")
        self.bar_btn.clicked.connect(self.draw_bar_chart)
        button_layout.addWidget(self.bar_btn)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def load_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "CSV 파일 선택", "", "CSV Files (*.csv)")
        if file_path:
            self.file_path = file_path
            QMessageBox.information(self, "성공", "CSV 파일이 성공적으로 불러와졌습니다.")

    def get_selected_stations(self):
        return [station for station, cb in self.station_checkboxes.items() if cb.isChecked()]

    def draw_line_chart(self):
        selected = self.get_selected_stations()
        if not selected:
            QMessageBox.warning(self, "경고", "하나 이상의 역을 선택해주세요.")
            return
        try:
            df = pd.read_csv(self.file_path, encoding='cp949')
            df = df[df['출발역'].isin(selected)]
            time_columns = df.columns[6:]
            pivot_df = df.groupby('출발역')[time_columns].mean().T

            plt.figure(figsize=(14, 7))
            for 역 in pivot_df.columns:
                plt.plot(pivot_df.index, pivot_df[역], marker='o', label=역)

            plt.title("선택된 역의 시간대별 평균 혼잡도 (선그래프)")
            plt.xlabel("시간대")
            plt.ylabel("혼잡도 지수")
            plt.xticks(rotation=45)
            plt.legend()
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.tight_layout()
            plt.show()
        except Exception as e:
            QMessageBox.critical(self, "오류", str(e))

    def draw_bar_chart(self):
        selected = self.get_selected_stations()
        if not selected:
            QMessageBox.warning(self, "경고", "하나 이상의 역을 선택해주세요.")
            return
        try:
            df = pd.read_csv(self.file_path, encoding='cp949')
            df = df[df['출발역'].isin(selected)]
            time_columns = df.columns[6:]
            pivot_df = df.groupby('출발역')[time_columns].mean()

            plt.figure(figsize=(16, 8))
            bar_width = 0.8 / len(pivot_df.index)
            index = range(len(time_columns))

            for i, station in enumerate(pivot_df.index):
                plt.bar(
                    [x + i * bar_width for x in index],
                    pivot_df.loc[station],
                    bar_width,
                    label=station
                )

            plt.xticks([x + bar_width * len(pivot_df.index) / 2 for x in index], time_columns, rotation=45)
            plt.title("선택된 역의 시간대별 평균 혼잡도 (막대그래프)")
            plt.xlabel("시간대")
            plt.ylabel("혼잡도 지수")
            plt.legend()
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            plt.tight_layout()
            plt.show()
        except Exception as e:
            QMessageBox.critical(self, "오류", str(e))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SubwayCongestionApp()
    window.show()
    sys.exit(app.exec_())
