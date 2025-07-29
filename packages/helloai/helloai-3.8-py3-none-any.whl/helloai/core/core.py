import __main__
import os
import sys
import builtins
import time
import math

# from threading import Event, Thread
import cv2
import keyboard

from threading import Thread

from .singlestore import SingleStore
from .colors import Color

import warnings
warnings.filterwarnings("ignore")



__all__ = [
    "loop",
    "setup",
    "run",
    "wait_key",
    "key_pressed",
    "is_pressed",
    "delay",
    "wait",
    "frame_rate",
    "size",
    "noloop",
    "stop",
    "end",
]

KEY_TABLE = [
    "nul",
    "soh",
    "stx",
    "etx",
    "eot",
    "enq",
    "ack",
    "bel",
    "bs",
    "tab",
    "lf",
    "vt",
    "ff",
    "cr",
    "so",
    "si",
    "dle",
    "dc1",
    "dc2",
    "dc3",
    "dc4",
    "nak",
    "syn",
    "etb",
    "can",
    "em",
    "sub",
    "esc",
    "fs",
    "gs",
    "rs",
    "us",
    "space",
    "!",
    '"',
    "#",
    "$",
    "%",
    "&",
    "'",
    "(",
    ")",
    "*",
    "+",
    ",",
    "-",
    ".",
    "/",
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    ":",
    ";",
    "<",
    "=",
    ">",
    "?",
    "@",
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
    "[",
    "\\",
    "]",
    "^",
    "_",
    "`",
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "l",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
    "{",
    "|",
    "}",
    "~",
    "del",
]


loop_flag = True
noloop_flag = False

setup_method = None
loop_method = None
end_method = None
key_pressed_method = None
mouse_event_method = None
# cancel_future_calls = None
mouse_down_time = time.time()

loop_frame_rate = 60
single_store = SingleStore()
builtins.mouse_event = None

# 전역 참조
builtins.mouse_x = 0
builtins.mouse_y = 0
builtins.pmouse_x = 0
builtins.pmouse_y = 0
builtins.fps = 0

builtins.mouse_pressed = False

builtins.WIDTH = 640
builtins.HEIGHT = 480
builtins.COLOR = Color.DEFAULT
builtins.pressed_key = 'wow'

builtins.windows = []


prev_time = 0
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

def __put_fps():
    global prev_time

    cur_time = time.time()
    sec = cur_time - prev_time
    prev_time = cur_time
    fps_val = 1 / (sec)
    fps_val = round(fps_val)
    builtins.fps = fps_val
    # fps_txt = "%01.f" % fps_val


def bye():
    global loop_flag
    loop_flag = False
    # delay(1)
    # if len(builtins.windows) > 0:
    #     builtins.windows = []
    #     cv2.destroyAllWindows()
    # print(builtins.windows)

    # for name in builtins.windows:
    #     cv2.destroyWindow(name)

    builtins.windows = []
    end_method()

    # cv2.destroyAllWindows()
    # end_method()
    print('👽 __bye__')
    sys.exit()


def stop():
    bye()

# 키보의 Control + C 를 예약한다. 
keyboard.add_hotkey("ctrl+c", bye)


# def call_repeatedly(interval, func, *args):
#     stopped = Event()

#     def loop():
#         while not stopped.wait(interval):   # the first call is in `interval` secs
#             func(*args)
#     Thread(target=loop).start()
#     return stopped.set


def size(width, height):
    builtins.WIDTH = width
    builtins.HEIGHT = height


def setup():
    pass


def loop():
    pass


def end():
    pass


def key_pressed(key):
    # q를 눌렀을 때 프로그램 종료하는 기능은 삭제한다. 
    if key == "esc":
        bye()

def is_pressed(key):
    return keyboard.is_pressed(key)


def __key_pressed(key):
    if key == "esc":
        # 프로그램에서 종료 처리를 하도록 해준다
        if key_pressed_method:
            key_pressed_method(key)
        bye()

    else:
        if key_pressed_method:
            key_pressed_method(key)
    


def mouse_event(name, event, x, y, flags=None, params=None):
    global mouse_down_time
    global mouse_x
    global mouse_y

    event_name = None
    if event == cv2.EVENT_LBUTTONDOWN:
        event_name = "left-down"
        builtins.mouse_pressed = True
        mouse_down_time = time.time()
    elif event == cv2.EVENT_LBUTTONUP:
        builtins.mouse_pressed = False
        diff = time.time() - mouse_down_time
        if diff < 0.1:
            event_name = "click"
        else:
            event_name = "left-up"
    elif event == cv2.EVENT_RBUTTONDOWN:
        event_name = "right-down"
    elif event == cv2.EVENT_RBUTTONUP:
        event_name = "right-up"
    elif event == cv2.EVENT_MOUSEMOVE:
        event_name = "move"

    builtins.mouse_x = x
    builtins.mouse_y = y

    if hasattr(__main__, "mouse_event"):
        if event_name is not None:
            __main__.mouse_event(name, event_name, x, y)


def delay(ms):
    """
    ms가 0일때는 아무키 입력할때 까지 기다림
    """
    if ms == 0:
        if len(builtins.windows) > 0:
            cv2.waitKey(0)
        else:
            time.sleep(60 * 60 * 1000 / 1000.0)  # 1hr
    else:
        if len(builtins.windows) > 0:
            cv2.waitKey(int(ms))
        else:
            time.sleep(float(ms) / 1000.0)

def wait(ms):
    """
    ms가 0일때는 아무키 입력할때 까지 기다림
    """
    delay(ms)


def wait_key(ms):

    if ms == 0:
        if len(builtins.windows) > 0:
            key = cv2.waitKey(ms)
            if key == 27:
                bye()
            else:
                __key_pressed(chr(key))
            return key
        else:
            key = input("press any key and enter: ")
            __key_pressed(key)
            return key
    else:
        key = cv2.waitKey(ms)
        if key == 27:
            bye()
        else:
            __key_pressed(chr(key))
        return key


def noloop():
    global noloop_flag
    noloop_flag = True


def print_pressed_keys(e):
    __key_pressed(e.name)


keyboard.hook(print_pressed_keys)


def run():
    global loop_flag
    global noloop_flag
    global setup_method
    global loop_method
    global end_method

    global key_pressed_method
    global cancel_future_calls

    if hasattr(__main__, "setup"):
        setup_method = __main__.setup
    else:
        setup_method = setup

    if hasattr(__main__, "loop"):
        loop_method = __main__.loop
    else:
        loop_method = loop

    if hasattr(__main__, "end"):
        end_method = __main__.end
    else:
        end_method = end

    if hasattr(__main__, "key_pressed"):
        key_pressed_method = __main__.key_pressed
    else:
        key_pressed_method = key_pressed

    # if hasattr(__main__, 'mouse_event'):
    #     mouse_event_method = __main__.mouse_event
    # else:
    #     mouse_event_method = mouse_event

    # single_store.mouse_event = mouse_event_method
    # single_store.mouse_event = mouse_event
    builtins.mouse_event = mouse_event

    # KeyBoard
    # if os.name != 'posix':
    #     listener = keyboard.Listener(
    #         on_press=on_press,
    #         on_release=on_release)
    #     listener.start()

    builtins.key_pressed = __key_pressed

    # 실행
    setup_method()
    while loop_flag:
        try:
            frame_exe_time = 1 / loop_frame_rate * 1000
            start = time.time()

            # pfs
            __put_fps()
            loop_method()
            builtins.pmouse_x = builtins.mouse_x
            builtins.pmouse_y = builtins.mouse_y

            delay(1)
            # key = cv2.waitKey(1)
            # print('Key.......', key)
            # if key == 27:
            #     bye()
            # elif key != -1 and key != 0:
            #     key_str = KEY_TABLE[key]
            #     __key_pressed(key_str)
            # delay(1)
            run_time = time.time() - start
            # print('loop_frame_rate ', loop_frame_rate)
            # print('frame_exe_time', frame_exe_time)
            # print('run_time ', run_time)
            # print('delay time ', frame_exe_time - run_time)
            delay_time = frame_exe_time - run_time
            if delay_time > 0:
                delay(delay_time)

        except KeyboardInterrupt:
            exit()

        if noloop_flag:
            loop_flag = False
            # 동시에 끝나지 않고, 실행이 끝난 상태를 유지한다.
            # wait_key(0)
            exit()


def frame_rate(value):
    """
    대략적인 프레임 속도를 지정한다.
    """
    global loop_frame_rate
    loop_frame_rate = value
