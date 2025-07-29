#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
import cv2
import numpy as np
import mediapipe as mp
from helloai.core.image import Image

# import absl.logging
# absl.logging.set_verbosity(absl.logging.ERROR)

__all__ = ["HandsDetector"]
tip_ids = [4, 8, 12, 16, 20]


class HandsDetector:
    def __init__(self):
        self.__mp_drawing = mp.solutions.drawing_utils
        self.__mp_hands = mp.solutions.hands
        self.__hands = self.__mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )
        self.__landmarks = []
        self.__angles = []
        self.__draw = True

    def load_model(self):
        pass

    def process(self, image, draw=True,line_width=4, circle_radius=6, draw_color=[(255, 0, 0), (192, 192, 192)]):
        self.__draw = draw

        image = image.frame
        h, w, c = image.shape

        # 입력되는 이미지가 거울 형식
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = self.__hands.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            self.__landmarks = []
            angles = []
            handness = self.__handness(results)
            for hand_landmarks in results.multi_hand_landmarks:
                lmks = []
                joint = np.zeros((21, 3))

                if self.__draw:
                    rgb1 = draw_color[0];
                    rgb2 = draw_color[1];

                    self.__mp_drawing.draw_landmarks(
                        image,
                        hand_landmarks,
                        self.__mp_hands.HAND_CONNECTIONS,
                        self.__mp_drawing.DrawingSpec(
                            color=(rgb1[2], rgb1[1], rgb1[0]), thickness=line_width, circle_radius=circle_radius
                        ),
                        self.__mp_drawing.DrawingSpec(
                            color=(rgb2[2], rgb2[1], rgb2[0]), thickness=line_width, circle_radius=circle_radius
                        ),
                    )

                for id, lm in enumerate(hand_landmarks.landmark):
                    px, py, pz = (
                        int(lm.x * w),
                        int(lm.y * h),
                        int(lm.z * w),
                    )  # 이미지 크기 기준으로 변환, Z값은 이미지의 너비를 이용해서 스케일링 했다. 
                    lmks.append((px, py, pz))
                    joint[id] = (px, py, pz)

                angle = self.__find_angle(joint)
                angles.append(angle)
                self.__landmarks.append(lmks)
        else:
            self.__landmarks = []
            handness = []
            angles = []

        result = []
        if len(self.__landmarks) > 0:
            result = self.__landmarks[0]  # 한쪽 손만 사용...

        return Image(image), result

    def __handness(self, results):
        ret = []
        for handness in results.multi_handedness:
            ret.append(handness.classification[0].label.lower())
        return ret

    def __find_angle(self, joint):
        self.__angles = []
        # Compute angles between joints
        v1 = joint[
            [0, 1, 2, 3, 0, 5, 6, 7, 0, 9, 10, 11, 0, 13, 14, 15, 0, 17, 18, 19], :
        ]  # Parent joint
        v2 = joint[
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], :
        ]  # Child joint
        v = v2 - v1  # [20,3]
        # Normalize v
        v = v / np.linalg.norm(v, axis=1)[:, np.newaxis]

        # Get angle using arcos of dot product
        angle = np.arccos(
            np.einsum(
                "nt,nt->n",
                v[[0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13, 14, 16, 17, 18], :],
                v[[1, 2, 3, 5, 6, 7, 9, 10, 11, 13, 14, 15, 17, 18, 19], :],
            )
        )  # [15,]
        self.__angles = np.degrees(angle)  # Convert radian to degree
        # data = np.array([angle], dtype=np.float32)
        return self.__angles.tolist()

    def fingers_up(self):
        if len(self.__landmarks) == 0:
            return [0, 0, 0, 0, 0]

        lmlist = self.__landmarks[0]
        fingers = []
        if len(lmlist) != 0:


            # 엄지 x값 비교
            if lmlist[tip_ids[0]][1] < lmlist[tip_ids[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            # y값 비교
            for i in range(1, 5):
                if lmlist[tip_ids[i]][2] < lmlist[tip_ids[i] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
        return fingers

    def distance(self, p1, p2, image, draw=True):
        image = image.frame
        r = 10
        t = 3
        x1, y1, _ = p1
        x2, y2, _ = p2
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv2.line(image, (x1, y1), (x2, y2), (255, 0, 255), t)
            cv2.circle(image, (x1, y1), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(image, (x2, y2), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(image, (cx, cy), r, (0, 0, 255), cv2.FILLED)
        length = math.hypot(x2 - x1, y2 - y1)

        return length, Image(image), [x1, y1, x2, y2, cx, cy]

    def __del__(self):
        """
        del handsdetector
        """
        if self.__hands:
            self.__hands.close()
