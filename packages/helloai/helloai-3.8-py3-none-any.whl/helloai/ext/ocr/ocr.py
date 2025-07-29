import os
import cv2
import easyocr
from helloai.core.image import Image
from PIL import Image as PIMage
from PIL import ImageFont, ImageDraw
import numpy as np

__all__ = ["OCR"]

FONT_PATH = "./assets/fonts/gulim.ttc"
FONT = ImageFont.truetype(FONT_PATH, 20)  # 원하는 폰트 크기로 설정

class OCR:
    def __init__(self):
        self.__reader = easyocr.Reader(['en', 'ko'])
        

    def readtext(self, img, isdraw=True):
        if not isinstance(img, Image) or img.image is None:
            return []

        frame = img.frame_.copy()
        # EasyOCR을 사용해 프레임에서 텍스트 인식
        results = self.__reader.readtext(frame)
        
        if isdraw :
            img_pil = PIMage.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            img_draw = ImageDraw.Draw(img_pil)

            # 인식된 텍스트가 있으면 프레임에 텍스트 표시
            for (bbox, text, prob) in results:
                # bbox는 텍스트 영역의 좌표 정보 (4개의 좌표로 구성된 리스트)
                (top_left, top_right, bottom_right, bottom_left) = bbox
                top_left = tuple(map(int, top_left))
                bottom_right = tuple(map(int, bottom_right))

                # 텍스트와 인식 확률 표시
                img_draw.rectangle([top_left, bottom_right], outline=(0, 255, 0), width=2)
                img_draw.text((top_left[0], top_left[1] - 20), f"{text} ({prob:.2f})", font=FONT, fill=(255, 0, 0))

            # PIL 이미지를 다시 OpenCV 이미지로 변환
            frame = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
            # 인식된 텍스트 데이터만 추출
            # recognized_texts = [text for (_, text, _) in results]

        return results, Image(frame)
    

    
