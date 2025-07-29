import csv

__all__ = ["CSVWriter"]


class CSVWriter:
    def __init__(self, filename="landmarks.csv", header=None):
        self.__filename = filename
        self.__header = header
        self.__row_len = 0

    def writerow(self, landmarks):
        # 헤더가 없을 때만 헤더를 기록한다. 
        if not self.__header:
            self.__row_len = len(landmarks)
            self.__header = [str(i+1) for i in range(len(landmarks))]

            with open(self.__filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(self.__header)  # CSV파일의 헤더에 임의의 헤더 넣기 

        # 데이터의 길이가 다르면 기록하지 않는다.
        if self.__row_len != len(landmarks):
            return 
        
        with open(self.__filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(landmarks)

