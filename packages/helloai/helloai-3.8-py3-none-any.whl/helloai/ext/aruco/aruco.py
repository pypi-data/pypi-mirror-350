# https://mecaruco2.readthedocs.io/en/latest/notebooks_rst/Aruco/aruco_basics.html
import cv2
import cv2.aruco as aruco
import numpy as np
import os
from helloai.core.image import Image

__all__ = ["ArUcoDetector"]


class ArUcoDetector:
    def __init__(self):
        self.__img = None
        self.__markers = None
        self.__type = cv2.aruco.DICT_4X4_50
        self.__aruco_dict = cv2.aruco.getPredefinedDictionary(self.__type)
        
        # DetectorParameters 객체 생성 및 파라미터 조정
        self.__parameters = cv2.aruco.DetectorParameters()


    def detect(self, img, draw=True):
        frame = img.frame.copy()

        if len(frame.shape) == 2:  # Grayscale image
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        elif frame.shape[2] == 4:  # RGBA image
            frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)

        # Convert the image to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # ArUco 마커 탐지
        corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(gray, self.__aruco_dict, parameters=self.__parameters)
        
        if ids is not None:
            print("Detected markers:", ids)
            if draw:
                cv2.aruco.drawDetectedMarkers(frame, corners, ids)

        return Image(frame)

    def generate(self, id=0, size=200):
        # ArUco 마커 생성
        marker = cv2.aruco.drawMarker(self.__aruco_dict, id, size)
        return Image(marker)

    # def augment(self, img, imgAug, drawId=True):
    #     # Loop through all the markers and augment each one
    #     frame = img.frame.copy()
    #     frame_over = imgAug.frame.copy()

    #     if len(self.__markers[0]) != 0:
    #         for bbox, id in zip(self.__markers[0], self.__markers[1]):
    #             frame = self.__draw(bbox, id, frame, frame_over)
    #     return Image(frame)

    def augment(self, bbox, id, img, imgAug, drawId=True):
        """
        :param bbox: the four corner points of the box
        :param id: maker id of the corresponding box used only for display
        :param img: the final image on which to draw
        :param imgAug: the image that will be overlapped on the marker
        :param drawId: flag to display the id of the detected markers
        :return: image with the augment image overlaid
        """

        frame = img.frame.copy()
        frame_over = imgAug.frame.copy()

        tl = bbox[0][0][0], bbox[0][0][1]
        tr = bbox[0][1][0], bbox[0][1][1]
        br = bbox[0][2][0], bbox[0][2][1]
        bl = bbox[0][3][0], bbox[0][3][1]

        # tl = bbox[0][0], bbox[0][1]
        # tr = bbox[1][0], bbox[1][1]
        # br = bbox[2][0], bbox[2][1]
        # bl = bbox[3][0], bbox[3][1]

        h, w, c = frame_over.shape

        pts1 = np.array([tl, tr, br, bl])
        pts2 = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
        matrix, _ = cv2.findHomography(pts2, pts1)
        frame_out = cv2.warpPerspective(
            frame_over, matrix, (frame.shape[1], frame.shape[0])
        )
        cv2.fillConvexPoly(frame, pts1.astype(int), (0, 0, 0))
        frame_out = frame + frame_out

        if drawId:
            cv2.putText(
                frame_out, str(id), tl, cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2
            )

        return Image(frame_out)