#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import argparse

import cv2
import numpy as np
import mediapipe as mp
from collections import deque

from helloai.core.image import Image

__all__ = ["FaceDetector"]


class FaceDetector:
    def __init__(self, min_detection_confidence=0.5):
        self.__is_model_loaded = False
        self.__face = None
        self.__landmarks = None
        self.__min_detection_confidence = min_detection_confidence
        self.__draw = True
        self.load_model()

    def load_model(self):
        if not self.__is_model_loaded:
            mp_face_detection = mp.solutions.face_detection
            self.__face = mp_face_detection.FaceDetection(
                min_detection_confidence=self.__min_detection_confidence
            )
            self.__is_model_loaded = True

    def process(self, img, draw=True):
        if not self.__is_model_loaded:
            print("모델이 준비되지 않았습니다")
            return img, []

        self.__draw = draw
        image = img.frame.copy()

        # 검출
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.__face.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        result = []

        # 그리기
        if results.detections is not None:
            for detection in results.detections:
                data = {}
                # data['id'] = detection.label_id

                brect = self.__calc_bounding_rect(
                    image, detection.location_data.relative_bounding_box, draw
                )
                data["bound"] = brect  # start_x, start_y, end_x, end_y

                debug_image, landmark_point = self.__draw_landmarks(
                    image, detection.location_data, draw
                )
                data["keypoints"] = landmark_point
                result.append(data)
        # # return Image(debug_image), result
        return Image(image), result

    def __calc_bounding_rect(self, image, bounding_box, draw):
        image_width, image_height = image.shape[1], image.shape[0]
        xmin = min(int(bounding_box.xmin * image_width), image_width - 1)
        ymin = min(int(bounding_box.ymin * image_height), image_height - 1)

        width = min(int(bounding_box.width * image_width), image_width - 1)
        height = min(int(bounding_box.height * image_height), image_height - 1)

        if draw:
            cv2.line(image, (xmin, ymin), (xmin + width, ymin), (0, 255, 0), 2)
            cv2.line(
                image,
                (xmin + width, ymin),
                (xmin + width, ymin + height),
                (0, 255, 0),
                2,
            )
            cv2.line(
                image,
                (xmin + width, ymin + height),
                (xmin, ymin + height),
                (0, 255, 0),
                2,
            )
            cv2.line(image, (xmin, ymin + height), (xmin, ymin), (0, 255, 0), 2)

        return [xmin, ymin, xmin + width, ymin + height]

    def __draw_landmarks(self, image, location_data, draw):
        image_width, image_height = image.shape[1], image.shape[0]
        landmark_point = []

        for index, landmark in enumerate(location_data.relative_keypoints):
            

            landmark_x = min(int(landmark.x * image_width), image_width - 1)
            landmark_y = min(int(landmark.y * image_height), image_height - 1)

            landmark_point.append((landmark_x, landmark_y))
            if draw:
                if index == 0:  # left eye
                    cv2.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
                if index == 1:  # right eye
                    cv2.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
                if index == 2:  # nose
                    cv2.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
                if index == 3:  # mouth
                    cv2.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
                if index == 4:  # left ear
                    cv2.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
                if index == 5:  # right ear
                    cv2.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        return image, landmark_point
