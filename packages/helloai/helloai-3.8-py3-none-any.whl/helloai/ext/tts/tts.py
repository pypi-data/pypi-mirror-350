import pyttsx3
import threading

__all__ = ["TTS"]

class TTS:
    def __init__(self):
        self.__engine = pyttsx3.init()
        self.__rate = 200  # 속도 설정 (기본 속도는 200)
        self.__volume = 1.0 # # 볼륨 설정 (기본 값은 1.0, 범위는 0.0에서 1.0)
        self.__voiceid = 1 #  0: 남성, 1: 여성
        self.__voices = self.__engine.getProperty('voices')
        
        self.__engine.setProperty('rate', self.__rate)  # 속도를 150으로 설정
        self.__engine.setProperty('volume', self.__volume)  # 볼륨을 90%로 설정
        self.__engine.setProperty('voice', self.__voices[self.__voiceid].id)

        self.__thread = None

    def __say(self, text):
        self.__engine.say(text)
        self.__engine.runAndWait()
    

    def say(self, text):
        self.__thread = threading.Thread(target=self.__say, args=(text,))
        self.__thread.setDaemon(True)  # 데몬 스레드로 설정, 프로그램을 끝낼때 정상적으로 메인이 종료될 수 있도록 
        self.__thread.start()

    def is_saying(self):
        if self.__thread :
            return self.__thread.is_alive()
        else:
            return False
    
    def __del__(self):
        # 객체가 삭제될 때 실행되는 코드
        print(f"{self.name} 객체가 삭제되었습니다.")
        if self.__thread:
            self.__thread.se



# 현재 영어만 대응된다. 구글 gtts는 mp3파일을 만들어서 재생한다. 미디어 플레이가 실행된다.
# from helloai import *

# win = Window("wnd")
# # 카메라 객체
# camera = Camera()
# tts = TTS()


# def loop():
#     img = camera.read()

#     if not tts.is_saying():
#         tts.say('안녕하세요')

#     # 윈도우에 이미지 표시 
#     win.show(img)
    

# # ---------------------------------------
# # For HelloAI
# # ---------------------------------------
# if __name__ == "__main__":
#     run()
