import matplotlib.pyplot as plt
import time
from helloai import *

__all__ = ["LineplotWindow"]

# 그래프 하단의 툴바 제거
plt.rcParams['toolbar'] = 'none'


class LineplotWindow:
    def __init__(self, title='', xlim=(0, 100), ylim=(0, 100), color=(255, 0, 0), type="scatter"):
        # 그래프 초기 설정
        self.title = title
        self.fig, self.ax = plt.subplots()
        self.x_data, self.y_data = [], []
        
        self.plot_type = type  # 그래프 유형 설정
        
        # RGB 값을 0-1 사이의 값으로 변환
        self.color = tuple(c / 255 for c in color)

        # plot_type에 따라 그래프 스타일 설정
        if self.plot_type == "line" or self.plot_type == "scatter":
            self.line, = self.ax.plot([], [], lw=2, color=self.color)  # 선 그래프 객체 생성

        # 축 설정
        self.ax.set_xlim(*xlim)
        self.ax.set_ylim(*ylim)
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Value")
        self.ax.set_title(self.title)

        # 창 닫기 버튼 이벤트 연결
        self.fig.canvas.manager.window.protocol("WM_DELETE_WINDOW", self.__hide_window)

        # 경과 시간 기록 시작
        self.start_time = time.time()
        self.__show()

    def __hide_window(self):
        pass
    def title(self, title):
        # 그래프 타이틀 설정
        self.ax.set_title(title)

    def add_data(self, y):
        # 새로운 데이터 추가
        x = time.time() - self.start_time  # 경과 시간 계산
        self.x_data.append(x)
        self.y_data.append(y)
    
    def update(self):
        # 축 범위 갱신 (필요 시)
        if self.x_data[-1] > self.ax.get_xlim()[1] - 10:
            self.ax.set_xlim(0, self.x_data[-1] + 10)
        
        # 그래프 유형에 따라 업데이트
        if self.plot_type == "line":
            # 선 그래프 업데이트
            self.line.set_data(self.x_data, self.y_data)
        
        elif self.plot_type == "scatter":
            # 점과 선을 함께 그리기 위해 축을 초기화하지 않음
            self.line.set_data(self.x_data, self.y_data)  # 선 그래프 업데이트
            self.ax.scatter(self.x_data[-1], self.y_data[-1], color=self.color)  # 새 점만 추가
        
        # 그래프 갱신
        self.fig.canvas.draw()
        plt.pause(0.01)  # 약간의 지연을 주어 갱신을 반영
    
    def __show(self):
        # 플롯 창을 보여주기 위한 메서드
        plt.show(block=False)
    

    def end(self):
        # 그래프 창 닫기
        plt.close(self.fig)

# ------------------------------------------------------------------
# 클래스 인스턴스 생성
# plot = RealTimeSensorPlot(color='green')  # 그래프 색상 설정
# plot.show()

# # 외부에서 데이터 추가 및 그래프 갱신 테스트
# import random
# for _ in range(10):
#     new_data = random.uniform(0, 100)  # 새 데이터 생성
#     plot.add_data(new_data)  # 데이터 추가
#     plot.update_plot()  # 그래프 업데이트
#     time.sleep(0.5)  # 0.5초 대기

# # 그래프 종료
# plot.end()
