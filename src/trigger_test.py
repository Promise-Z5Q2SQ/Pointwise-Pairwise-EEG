from ctypes import *
import time

# pdll = windll.inpoutx64
base_code = 0xBFF8


def send_trigger(code):
    # pdll.Out32(base_code, code)
    time.sleep(0.01)
    # pdll.Out32(base_code, 0)


def test():
    t = range(1, 200)
    for i in range(1000):
        send_trigger(t[i % 200])
        time.sleep(0.5)


if __name__ == '__main__':
    test()
