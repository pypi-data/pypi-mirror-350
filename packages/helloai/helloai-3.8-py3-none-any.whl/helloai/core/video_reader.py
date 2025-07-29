
import cv2
from helloai.core.image import Image
from helloai.core.api import new_image

__all__ = ["VideoReader"]

class VideoReader:
    def __init__(self, path):
        self.__path = path
        self.__capture = cv2.VideoCapture(self.__path)

        # 비디오가 열리지 않으면 예외를 발생
        if not self.__capture.isOpened():
            raise ValueError(f"Could not open the video file: {self.__path}")

        # 비디오 속성 설정
        self.__width = int(self.__capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.__height = int(self.__capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.__fps = self.__capture.get(cv2.CAP_PROP_FPS)
        self.__frame_count = int(self.__capture.get(cv2.CAP_PROP_FRAME_COUNT))
        self.end_ = False

    def read(self):
        """
        다음 프레임을 읽어옵니다.
        Returns:
            (ret, frame): 성공적으로 프레임을 읽으면 True와 프레임을 반환하고,
            그렇지 않으면 False와 None을 반환합니다.
        """
        ret, frame = self.__capture.read()
        if frame is None:
            self.end_ = True
            frame = new_image(color=(0, 0, 0)).frame

        return Image(frame)


    def release(self):
        if self.__capture is not None:
            self.__capture.release()
            self.__capture = None

    def __del__(self):
        self.release()


    def get_info(self):
        """
        비디오의 기본 정보를 반환합니다.
        Returns:
            dict: 비디오의 너비, 높이, FPS, 총 프레임 수
        """
        return {
            "width": self.__width,
            "height": self.__height,
            "fps": self.__fps,
            "frame_count": self.__frame_count
        }