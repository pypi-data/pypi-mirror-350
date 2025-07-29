import matplotlib.pyplot as plt
import numpy as np
import time
from helloai import *

__all__ = ["TableWindow"]

# 그래프 하단의 툴바 제거
plt.rcParams['toolbar'] = 'none'


class TableWindow:
    def __init__(self, title='', columns=["Timestamp", "Sensor Value"], max_rows=15):
        self.fig, self.ax = plt.subplots()
        self.ax.axis('off')  # 축 비활성화

        self.max_rows = max_rows  # 표시할 최대 행 수
        self.font_size = 10  # 글자 크기 설정
        self.columns = columns
        self.data = [columns]  # 첫 행에 컬럼명 추가
        self.title = title

        # 초기 테이블 설정
        self.table = self.ax.table(cellText=[[""] * 2 for _ in range(self.max_rows)],
                                   colLabels=["Timestamp", "Sensor Value"],
                                   loc="center")
        
        # 테이블의 각 셀에 대해 글자 크기 설정
        self.table.auto_set_font_size(False)
        self.table.set_fontsize(self.font_size)
        self.table.scale(1, 1.2)  # 너비 1, 높이를 cell_height로 설정
        self.ax.set_title(self.title, fontsize=self.font_size + 2)

        self.__show()

    def __show(self):
        # 플롯 창을 보여주기 위한 메서드
        plt.show(block=False)

    def add_data(self, value):
        # 현재 시간과 센서 값을 추가
        timestamp = time.strftime("%H:%M:%S")
        self.data.append([timestamp, value])

        # 데이터가 최대 행 수를 넘으면 가장 오래된 데이터 제거
        if len(self.data) > self.max_rows:
            self.data.pop(1)


    def update(self):
        # 테이블의 각 셀을 업데이트
        for i, (timestamp, value) in enumerate(self.data):
            # 기본 셀 텍스트 색상 설정
            self.table[i, 0].get_text().set_text(timestamp)  # 타임스탬프 업데이트
            self.table[i, 1].get_text().set_text(str(value))  # 센서 값 업데이트
            self.table[i, 0].get_text().set_color("black")  # 기본 색상 검정
            self.table[i, 1].get_text().set_color("black")  # 기본 색상 검정
        
        # 마지막 행을 빨간색으로 설정
        if len(self.data) > 1:  # 데이터가 하나 이상 있는 경우에만
            self.table[len(self.data) - 1, 0].get_text().set_color("red")  # 타임스탬프 빨간색
            self.table[len(self.data) - 1, 1].get_text().set_color("red")  # 센서 값 빨간색

        # 남은 빈 행들을 초기화
        for i in range(len(self.data), self.max_rows):
            self.table[i, 0].get_text().set_text("")
            self.table[i, 1].get_text().set_text("")

        self.fig.canvas.draw()
        plt.pause(0.1)

    def end(self):
        plt.close(self.fig)
        print("그래프 표시가 종료되었습니다.")

