#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import cv2
import mediapipe as mp

from helloai.core.image import Image

__all__ = ["FaceDetector"]

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh

# 색상 설정을 위해 DrawingSpec 객체 생성
tesselation_spec = mp_drawing.DrawingSpec(color=(192, 192, 192), thickness=1)  # 초록색
contours_spec = mp_drawing.DrawingSpec(color=(192, 192, 192), thickness=1)     # 빨간색
iris_spec = mp_drawing.DrawingSpec(color=(192, 192, 192), thickness=1)         # 파란색

#  인덱스 번호 참조
#  https://www.kaggle.com/discussions/questions-and-answers/393052
LANDMARK_INDICES_68 = [
    # FACEMESH_FACE_OVAL
    10, 356, 152, 127,

    # FACEMESH_RIGHT_EYEBROW (미디어파이프는 우리와 왼쪽 오른쪽이 반대임.)
    46, 52, 55,

    # FACEMESH_LEFT_EYEBROW
    285, 282, 276,

    # FACEMESH_LEFT_EYE (미디어파이프는 우리와 왼쪽 오른쪽이 반대임.)
    33, 159, 155, 145,

    # FACEMESH_RIGHT_EYE
    382, 386, 263, 374,
    # NOSE
    5, 4,
    # FACEMESH_LIPS
    61, 13, 409, 14,
];

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
            self.__face = mp_face_mesh.FaceMesh(
                max_num_faces=1,
                refine_landmarks=True,
                min_detection_confidence=self.__min_detection_confidence,
                min_tracking_confidence=self.__min_detection_confidence
            )
            self.__is_model_loaded = True

    def process(self, img, draw=True):
        self.__landmarks = []

        if not self.__is_model_loaded:
            print("모델이 준비되지 않았습니다")
            return img, []

        self.__draw = draw
        image = img.frame.copy()

        # 검출
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.__face.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # 얼굴을 검출하지 못했을 경우
        if not results.multi_face_landmarks:
            return img, []

        # 이미지 너비, 높이 
        image_width, image_height = image.shape[1], image.shape[0]
        landmark_point = []

        for face_landmarks in results.multi_face_landmarks:
            # 각 포인트 처리 
            for landmark in face_landmarks.landmark:
                # 이미지 크기를 기준으로 x, y 값을 픽셀 단위로 변환
                x_px = int(landmark.x * image_width)
                y_px = int(landmark.y * image_height)
                
                # z 값은 상대 깊이로, 필요에 따라 크기를 조절하여 사용할 수 있음
                z_px = round(landmark.z * image_width)  # z 값을 이미지 폭 기준으로 스케일링
                
                # 변환된 좌표 추가
                self.__landmarks.append((x_px, y_px, z_px))

            # 각 얼굴마다 그리기 
            if draw:
                image, _ = self.__draw_landmarks(image, face_landmarks)
        
        # 필요한 포인트만 리턴한다면 여기서 필터링
        selected_landmarks = [self.__landmarks[i] for i in LANDMARK_INDICES_68]
        
        landmark_point = copy.deepcopy(self.__landmarks)
        return Image(image), selected_landmarks

    def __calc_bounding_rect(self, image, bounding_box, draw):
        pass

    def __draw_landmarks(self, image, face_landmarks):

        image_width, image_height = image.shape[1], image.shape[0]

        mp_drawing.draw_landmarks(
            image=image,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACEMESH_TESSELATION,
            landmark_drawing_spec=None,
            connection_drawing_spec=tesselation_spec)
        mp_drawing.draw_landmarks(
            image=image,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACEMESH_CONTOURS,
            landmark_drawing_spec=None,
            connection_drawing_spec=contours_spec)
        
        mp_drawing.draw_landmarks(
            image=image,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACEMESH_IRISES,
            landmark_drawing_spec=None,
            connection_drawing_spec=iris_spec)
        
        for idx in LANDMARK_INDICES_68:
            x = int(face_landmarks.landmark[idx].x * image_width)
            y = int(face_landmarks.landmark[idx].y * image_height)
            cv2.circle(image, (x, y), 4, (0, 0, 255), -1)  # 빨간색으로 채움 
            cv2.circle(image, (x, y), 4, (255, 255, 255), 2) # 외곽선 그림 

        return image, []
