import threading
import queue

__all__ = [
    "ThreadControl"
]

class ThreadControl:
    def __init__(self, board, queue, event):
        """파이썬 IDE에서 로봇을 동작시키기 위한 스레드 랩핑 

        Args:
            board: The robot's control board object, which has methods to control the display, etc.
        """
        self.board = board  # 로봇 제어 보드 객체
        self.gesture_queue = queue  # 손모양 인식 결과를 저장할 큐
        self.robot_done_event = event  # 로봇 동작 완료 이벤트
        self.stop_event = threading.Event()  # 스레드 종료 이벤트
        self.thread = threading.Thread(target=self._control_robot, daemon=True)  # 로봇 제어 스레드
        self.__coro = None

    def _control_robot(self):
        """
        Internal method to control the robot based on gestures in the queue.
        """
        while not self.stop_event.is_set():
            try:
                # 큐에서 손모양 인식 결과를 기다림
                gesture = self.gesture_queue.get(timeout=0.5)  # 0.5초 대기 후 타임아웃 발생
                self.__coro(gesture)

                # 로봇 동작 완료 알림
                self.gesture_queue.task_done()  # 작업 완료
                self.robot_done_event.set()  # 완료 이벤트 설정
            except queue.Empty:
                continue  # 큐가 비어 있으면 다음 루프로 이동

    def start(self, coro):
        """
        Start the robot control thread.
        """
        self.__coro = coro

        self.thread.start()

    def stop(self):
        """
        Stop the robot control thread.
        """
        self.stop_event.set()
        self.thread.join()

    def add_command(self, gesture):
        """
        Add a gesture to the queue for robot control.

        Args:
            gesture: The recognized gesture to be processed.
        """
        if self.robot_done_event.is_set():  # 로봇이 준비 상태일 때만 큐에 추가
            self.gesture_queue.put(gesture)
            self.robot_done_event.clear()
            # print(f"Gesture '{gesture}' added to queue.")
        else:
            # print(f"Robot not ready. Gesture '{gesture}' ignored.")
            pass

    def is_ready(self):
        return self.robot_done_event.is_set()
        