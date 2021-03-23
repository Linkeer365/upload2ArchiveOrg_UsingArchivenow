import win32gui
import win32con
import win32api
import win32clipboard
import os
import sys
import time

enter_code=0x0D
startAt=time.time()
while True:
    cur_time=time.time()
    delta_time=int(cur_time-startAt)
    print("delta_time:",delta_time)
    if (delta_time+14)%(60*5)==0:
        print("press!")
        win32api.keybd_event(enter_code, 0,0,0)
        time.sleep(.05)
        win32api.keybd_event(enter_code,0 ,win32con.KEYEVENTF_KEYUP ,0)
    time.sleep(40)